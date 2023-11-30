from datetime import date

from src.bot import AuthContractService
from src.common.services import Service
from src.dto import StudentRaw

__all__ = [
    "RegistrationService",
]


class RegistrationService(Service):
    async def register_student(self, student_raw: StudentRaw):
        async with self._con.transaction():
            auth_contract_service = AuthContractService(self._con)
            new_student = await auth_contract_service.create_student(student_raw)

            university = await auth_contract_service.find_university_by_alias(student_raw.university_alias)
            new_group = await auth_contract_service.create_or_return_group(
                student_raw.group_name,
                student_raw.telegram_id,
                university.id,
                date(day=1, month=1, year=3000),  # FIXME: Set correct payment data. It is neccecary for payment work.
            )

            await auth_contract_service.append_student_into_group(new_group, new_student)
