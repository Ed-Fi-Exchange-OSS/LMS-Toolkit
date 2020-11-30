import os
from typing import List, Optional


def _get_newest_file(directory: str) -> Optional[str]:
    if not os.path.exists(directory):
        return None

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


def get_system_activities_files(base_directory: str) -> List[str]:
    files = list()

    sys_activities = os.path.join(base_directory, "system-activities")

    if os.path.exists(sys_activities):
        for f in os.scandir(sys_activities):
            file = _get_newest_file(f.path)

            if file is not None:
                files.append(file)

    return files


def get_section_associations_file(
    base_directory: str, section_id: int
) -> Optional[str]:
    return _get_file_for_section(base_directory, section_id, "section-associations")


def get_section_activities_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_file_for_section(base_directory, section_id, "section-activities")


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
