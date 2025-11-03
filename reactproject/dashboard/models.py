from django.db import models
import uuid


class Announcements(models.Model):
    announcements_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey('auth.User', models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'announcements'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'


# ----------------------------------------
# 1️⃣ 환자 정보 테이블 (dbr_patients)
# ----------------------------------------
class DbrPatients(models.Model):
    SEX_CHOICES = [
        ('male', '남성'),
        ('female', '여성'),
    ]

    patient_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="환자 ID"
    )
    name = models.CharField(max_length=100, verbose_name="이름")
    birth_date = models.DateField(verbose_name="생년월일")
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, verbose_name="성별")
    resident_number = models.CharField(max_length=13, blank=True, null=True, verbose_name="주민등록번호")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="전화번호")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="주소")
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="신장(cm)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="체중(kg)")
    user_id = models.CharField(max_length=150, unique=True, verbose_name="로그인 ID")
    password = models.CharField(max_length=128, verbose_name="비밀번호")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        managed = True
        db_table = "dbr_patients"
        verbose_name = "환자"
        verbose_name_plural = "환자 목록"

    def __str__(self):
        return f"{self.name} ({self.user_id})"

    @property
    def is_authenticated(self):
        """DRF의 IsAuthenticated 권한 검사용"""
        return True

# ----------------------------------------
# 2️⃣ 혈액검사 결과 테이블 (dbr_blood_results)
# ----------------------------------------
class DbrBloodResults(models.Model):
    blood_result_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        DbrPatients,
        on_delete=models.CASCADE,
        related_name="blood_results",
        db_column="patient_id",
        verbose_name="환자 ID"
    )
    ast = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    alt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    alp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ggt = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bilirubin = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    albumin = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    inr = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    platelet = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    afp = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    albi = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    taken_at = models.DateField(verbose_name="검사일자")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        managed = True
        db_table = "dbr_blood_results"
        verbose_name = "혈액검사 결과"
        verbose_name_plural = "혈액검사 결과 목록"

    def __str__(self):
        return f"{self.patient.name} - {self.taken_at}"


# ----------------------------------------
# 3️⃣ 혈액검사 기준 테이블 (dbr_blood_test_references)
# ----------------------------------------
class DbrBloodTestReferences(models.Model):
    reference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="검사 항목명")
    normal_range_min = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    normal_range_max = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name="단위")
    description = models.TextField(blank=True, null=True, verbose_name="설명")

    class Meta:
        managed = True
        db_table = "dbr_blood_test_references"
        verbose_name = "혈액검사 기준"
        verbose_name_plural = "혈액검사 기준 목록"

    def __str__(self):
        return f"{self.name} ({self.unit or '-'})"


# ----------------------------------------
# 4️⃣ 일정관리 테이블 (dbr_appointments)
# ----------------------------------------
class DbrAppointments(models.Model):
    APPOINTMENT_TYPE_CHOICES = [
        ('blood_test', '혈액검사'),
        ('ct', 'CT 검사'),
        ('mri', 'MRI 검사'),
        ('ultrasound', '초음파 검사'),
        ('consultation', '진료 상담'),
        ('other', '기타'),
    ]

    STATUS_CHOICES = [
        ('scheduled', '예정'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]

    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        DbrPatients,
        on_delete=models.CASCADE,
        related_name="appointments",
        db_column="patient_id",
        verbose_name="환자 ID"
    )
    appointment_date = models.DateField(verbose_name="검사 일정")
    appointment_time = models.TimeField(blank=True, null=True, verbose_name="검사 시간")
    hospital = models.CharField(max_length=100, verbose_name="병원명")
    appointment_type = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPE_CHOICES,
        default='blood_test',
        verbose_name="검사 종류"
    )
    details = models.TextField(blank=True, null=True, verbose_name="자세한 내용")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name="상태"
    )
    reminder_enabled = models.BooleanField(default=True, verbose_name="알림 설정")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        managed = True
        db_table = "dbr_appointments"
        verbose_name = "검사 일정"
        verbose_name_plural = "검사 일정 목록"
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient.name} - {self.hospital} ({self.appointment_date})"

