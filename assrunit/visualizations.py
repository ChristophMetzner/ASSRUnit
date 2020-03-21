import numpy as np; np.random.seed(0)
import matplotlib.pylab as plt
import functools
import operator


from assrunit.db import *


def get_studies(ids=[], titles=[], authors=[], print_output=True):
    """Prints and returns list of studies.
       Where condition is concatenated on OR operator.

        Parameters
        -----------------
        ids:          list of integers. Studies IDs to filter the selection results
        titles:       list of strings. Studies titles to filter the selection results
        authors:      list of strings. Studies authors names to filter the selection results
        print_output: Bool. To print the output of the query

        Returns
        -----------------
        studies: peewee.ModelSelect
        """

    # Build 'where' terms using user provided filters
    where_term = [Studies.title.contains(title) for title in titles] if titles else []
    where_term += [Studies.authors.contains(author) for author in authors] if authors else where_term
    where_term += [Studies.ID << ids] if ids else where_term

    if where_term:

        # Add OR operator between terms
        where_term = functools.reduce(operator.or_, where_term)
        # PeeWee query
        studies = Studies.select().where(where_term)
    else:
        studies = Studies.select()

    # Print loop
    if print_output:
        for study in studies:
            print(f'\nID: {study.ID}\nTitle: {study.title}\nAuthors: {study.authors} \nYear: {study.year} ')

    return studies


def get_observations(power=[], drive=[], study_id=[], print_output=True):
    """Prints and returns list of experiments observations.
        Where condition is concatenated as  power AND drive OR study_id

        Parameters
        -----------------
        power:         list of numbers. To filter the selection results using StudiesExperiments.power
        drive:        list of numbers. To filter the selection results using StudiesExperiments.drive
        study_id:     list of integers. To filter the selection results using StudiesExperiments.study_id
        print_output: Bool. To print the output of the query

        Returns
        -----------------
        observations: peewee.ModelSelect

        """

    # Build 'where' terms using user provided filters
    where_term = [StudiesExperiments.power << power] if power else []
    where_term += [StudiesExperiments.drive << drive] if drive else where_term

    if where_term:
        # Add AND operator between terms
        where_term = functools.reduce(operator.and_, where_term)
        # PeeWee query
        observations = StudiesExperiments.select().where(where_term | StudiesExperiments.study_id << study_id)
    else:
        observations = StudiesExperiments.select()

    # Print loop
    if print_output:
        for experiment in observations:
            print(
                f'At ({experiment.power} Hz power at {experiment.drive} Hz drive) ' +
                f' Response value was {experiment.value} ' +
                f' in {Disorders.get(Disorders.ID == experiment.disorder_id).name} \n'
            )
    return observations


def experimental_qualitative_overview(power=[], drive=[], study_id=[], study_title=[], study_authors=[], plot_table=True):
    """Gives a qualitative overview of the experimental observations.

        Parameters
        -----------------
        power:         list of numbers. To filter the selection results using StudiesExperiments.power
        drive:         list of numbers. To filter the selection results using StudiesExperiments.drive
        study_id:      list of integers. To filter the selection results using StudiesExperiments.study_id
        study_title:   list of strings. To filter the selection results using Studies.title
        study_authors: list of strings. To filter the selection results using Studies.authors
        plot_table:    Results will be displayed in a table

        Returns
        -----------------
        Return term has been added as a comment to avoid strings prints on the output table

        qualitative_values: array of strings. Represents patients response values compared to Healthy controls values.
        col_labels:         distinct 'power,drive' pairs
        row_labels:         studies first-author-name_year
        """

    # Build 'where' terms using user provided filters
    where_term_OR = [Studies.title.contains(title) for title in study_title] if study_title else []
    where_term_OR += [Studies.authors.contains(author) for author in study_authors] if study_authors else where_term_OR
    where_term_OR += [Studies.ID << study_id] if study_id else where_term_OR

    where_term_AND = [StudiesExperiments.power << power] if power else []
    where_term_AND += [StudiesExperiments.drive << drive] if drive else where_term_AND

    # Add operators between terms
    where_term_OR = functools.reduce(operator.or_, where_term_OR) if where_term_OR else []
    where_term_AND = functools.reduce(operator.and_, where_term_AND) if where_term_AND else []

    # Query to select the needed data
    if where_term_OR and where_term_AND:
        experiments = StudiesExperiments.select().join(Studies).where((where_term_OR) | (where_term_AND))
    elif where_term_OR:
        experiments = StudiesExperiments.select().join(Studies).where((where_term_OR))
    elif where_term_AND:
        experiments = StudiesExperiments.select().join(Studies).where((where_term_AND))
    else:
        experiments = StudiesExperiments.select().join(Studies)

    # List distinct power and drive experiments to get rows labels
    experiments_power_drive = list({
                                       f'{experiment.power}-{experiment.drive}': experiment for experiment in
                                       experiments}.values()
                                   )

    row_labels = [f'{experiment.power} Hz power at {experiment.drive} Hz drive' for experiment in
                  experiments_power_drive]

    # List the returned experiments study_ids
    returned_study_ids = [s.study_id for s in experiments]

    # Unique list items
    returned_study_ids = set(returned_study_ids)

    # Select studies to get columns labels
    studies = Studies.select(Studies.ID, Studies.authors, Studies.year).where(
        Studies.ID << returned_study_ids).order_by(Studies.year.asc())
    col_labels = [f"{study.authors.split(',')[0]}_{study.year}" for study in studies]

    # Define empty arrays to save experiments values
    qualitative_values = np.ndarray((len(row_labels), len(col_labels)), dtype='U10')

    # Get healthy controls ID to be distinguished
    hc_id = [d.ID for d in Disorders.select(Disorders.ID).where(Disorders.name.contains('controls'))][0]

    # Get experiments values per power/drive
    for study_index, study in enumerate(studies):

        for index, value in enumerate(experiments_power_drive):

            experiment_result = StudiesExperiments.select(StudiesExperiments.value,
                                                          StudiesExperiments.disorder_id).where(
                StudiesExperiments.study_id == study.ID,
                StudiesExperiments.power == value.power,
                StudiesExperiments.drive == value.drive,
            )

            if not experiment_result:
                qualitative_values[index][study_index] = 'Not tested'
                continue

            hc_value = 0
            disorder_value = 0

            for result in experiment_result:
                if result.disorder_id == hc_id:
                    hc_value = result.value
                    continue
                disorder_value = result.value

            if hc_value < disorder_value:
                qualitative_values[index][study_index] = 'higher'

            elif hc_value > disorder_value:
                qualitative_values[index][study_index] = 'lower'

            else:
                qualitative_values[index][study_index] = 'equal'

    if plot_table:
        _plot_table(qualitative_values, row_labels, col_labels)

    return qualitative_values, row_labels, col_labels


def get_meta(study_id):
    """Prints information about the study measurements and participants.

        Parameters
        -----------------
        study_id: int study identifier

        Returns
        -----------------
        """

    experiment_data = StudiesMeasurements.select().where(StudiesMeasurements.study_id == study_id)
    participant_data = SubjectsGroups.select().where(SubjectsGroups.study_id == study_id)
    study_data = Studies.select().where(Studies.ID == study_id)

    print(f'Study:\n{study_data[0].title}. {study_data[0].authors}. {study_data[0].year} \n')

    print(f'Participant Data:') if participant_data else []

    for info in participant_data:
        sex = 'Female' if info.sex == 'F' else 'Male'
        print(f'{[disorder.name for disorder in (Disorders.select().where(Disorders.ID == info.disorder_id))][0]}')
        print(f'{info.count}' +
              f' {sex}' +
              f'\nMean age={info.mean_age} years and ' +
              f'mean illness duration={info.mean_illness_duration} years\n'
              )

    for info in experiment_data:
        print(f'Modality: {info.modality}\nLocation: {info.location}')
        print(f'Signal Processing methods: {info.processing}')
        print(f'Response value calculated as: {info.value}\n')


def plot_statistics(stats, row_labels, col_labels):
    """

        Parameters
        -----------------

        Returns
        -----------------

        """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.table(cellText=stats, rowLabels=row_labels, colLabels=col_labels, loc="center")
    ax.axis("off")


def _plot_table(cell_text, row_labels, col_labels):
    """Plot table

        Parameters
        -----------------
        cell_text:  Table cell values and table content
        row_labels: Table rows labels
        col_labels: Table columns labels

        Returns
        -----------------

        """
    table = plt.table(
        cellText=cell_text, rowLabels=row_labels, colLabels=col_labels, loc="top",
        bbox=[1, 0.5, 5, 1], cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(18)
    table.scale(4, 4)

    plt.axis("off")


def boxplot(data, labels):
    """Simple box plot function.

        Parameters
        -----------------
        data   : ndarray
                nD array containing the data.
        labels : list
                A list containing the axis labels.
        """
    plt.boxplot(data, labels=labels, showmeans=True)
    # plt.show()




