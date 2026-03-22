from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    help = "Wait for database to be available"

    def handle(self, *args, **options):
        max_attempts = 30
        wait_seconds = 2

        self.stdout.write("Waiting for database...")
        
        for attempt in range(1, max_attempts+1):
            try:
                db_conn = connections["default"]
                # 커서를 생성하고 간단한 쿼리를 실행해서 실제 DB 연결 가능 여부 확인
                with db_conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return

            except OperationalError:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  {attempt}회차 연결 실패. {wait_seconds}초 후 재시도...')
                )
                time.sleep(wait_seconds)

        raise CommandError("Database connection failed after all attempts")