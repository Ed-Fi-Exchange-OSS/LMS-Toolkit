import os
from typing import Optional


def _get_newest_file(directory: str) -> Optional[str]:
    if not os.path.exists(directory):
        return ""

    files = [(f.path, f.name) for f in os.scandir(directory) if f.name.endswith(".csv")]
    files = sorted(files, key=lambda x: x[1], reverse=True)

    if len(files) > 0:
        return files[0][0]

    return None


def _get_file_for_section(
    base_directory: str, section_id: int, file_type: str
) -> Optional[str]:
    return _get_newest_file(
        os.path.join(base_directory, f"section={section_id}", file_type)
    )


def get_users_file(base_directory: str) -> Optional[str]:
    return _get_newest_file(os.path.join(base_directory, "users"))


def get_sections_file(base_directory: str) -> Optional[str]:
    return _get_newest_file(os.path.join(base_directory, "sections"))


def get_section_associations_file(
    base_directory: str, section_id: int
) -> Optional[str]:
    return _get_file_for_section(base_directory, section_id, "section-associations")


def get_user_activities_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_file_for_section(base_directory, section_id, "user-activities")


def get_assignments_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_file_for_section(base_directory, section_id, "assignments")


def get_grades_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_file_for_section(base_directory, section_id, "grades")


def get_submissions_file(
    base_directory: str, section_id: int, assignment_id: int
) -> Optional[str]:
    path = os.path.join(
        base_directory,
        f"section={section_id}",
        f"assignment={assignment_id}",
        "submissions",
    )
    return _get_newest_file(path)


def get_attendance_events_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_file_for_section(base_directory, section_id, "attendance-events")
