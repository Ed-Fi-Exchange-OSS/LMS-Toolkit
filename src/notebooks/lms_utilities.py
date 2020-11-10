import os
from typing import Callable, Optional

import pandas as pd


# Filesystem functions
def _get_newest_file(directory: str) -> Optional[str]:
    if not os.path.exists(directory):
        return ""

    files = [(f.path, f.name) for f in os.scandir(directory) if f.name.endswith(".csv")]
    files = sorted(files, key=lambda x: x[1], reverse=True)

    if len(files) > 0:
        return files[0][0]

    return None

def _get_file_for_section(base_directory: str, section_id: int, file_type: str) -> str:
    return _get_newest_file(os.path.join(base_directory, f"section={section_id}", file_type))

def get_users_file(base_directory: str) -> str:
    return _get_newest_file(os.path.join(base_directory, "users"))

def get_sections_file(base_directory: str) -> str:
    return _get_newest_file(os.path.join(base_directory, "sections"))

def get_section_associations_file(base_directory: str, section_id: int) -> str:
    return _get_file_for_section(base_directory, section_id, "section-associations")

def get_user_activities_file(base_directory: str, section_id: int) -> str:
    return _get_file_for_section(base_directory, section_id, "user-activities")

def get_assignments_file(base_directory: str, section_id: int) -> str:
    return _get_file_for_section(base_directory, section_id, "assignments")

def get_grades_file(base_directory: str, section_id: int) -> str:
    return _get_file_for_section(base_directory, section_id, "grades")

def get_submissions_file(base_directory: str, section_id: int, assignment_id: int) -> str:
    path = os.path.join(base_directory, f"section={section_id}", f"assignment={assignment_id}", "submissions")
    return _get_newest_file(path)

def get_attendance_events_file(base_directory: str, section_id: int) -> str:
    return _get_file_for_section(base_directory, section_id, "attendance-events")

# DataFrame functions
def _read_csv(file: str) -> pd.DataFrame:
    if file:
        return pd.read_csv(file, engine="c", parse_dates=True, infer_datetime_format=True)

    return pd.DataFrame()

def get_all_users(base_directory: str) -> pd.DataFrame:
    file = get_users_file(base_directory)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def get_all_sections(base_directory: str) -> pd.DataFrame:
    file = get_sections_file(base_directory)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def get_section_associations(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_section_associations_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def _get_data_for_section(base_directory: str, sections: pd.DataFrame, callback: Callable) -> pd.DataFrame:
    df = pd.DataFrame()

    if sections.empty:
        print("No sections have been loaded, therefore no section sub-files can be read.")
        return

    for _, section_id in sections[["SourceSystemIdentifier"]].itertuples():
        sa = callback(base_directory, section_id)

        if not sa.empty:
            df = df.append(sa)

    return df

def get_all_section_associations(base_directory: str, sections: pd.DataFrame) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_section_associations)

def get_user_activities(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_user_activities_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def get_all_user_activities(base_directory: str, sections: pd.DataFrame) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_user_activities)

def get_assignments(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_assignments_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def get_all_assignments(base_directory: str, sections: pd.DataFrame) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_assignments)

def get_submissions(base_directory: str, section_id: int, assignment_id: int) -> pd.DataFrame:
    file = get_submissions_file(base_directory, section_id, assignment_id)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def get_all_submissions(base_directory: str, assignments: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    columns = ["SourceSystemIdentifier", "LMSSectionSourceSystemIdentifier"]
    for _, assignment_id, section_id  in assignments[columns].itertuples():
        s = get_submissions(base_directory, section_id, assignment_id)

        if not s.empty:
            df = df.append(s)

    return df

def get_grades(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_grades_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def get_all_grades(base_directory: str, sections: pd.DataFrame) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_grades)

def get_attendance_events(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_attendance_events_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return pd.DataFrame()

def get_all_attendance_events(base_directory: str, sections: pd.DataFrame) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_attendance_events)
