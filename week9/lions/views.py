from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Lion, Task, LionProfile, Tag


# ── Lion CRUD ──────────────────────────────────────────────────────────────────

def lion_list(request):
    """아기사자 목록"""
    lions = Lion.objects.all()
    return render(request, 'lions/lion_list.html', {'lions': lions})


@transaction.atomic
def lion_create(request):
    """
    아기사자 등록
    - Lion 생성과 동시에 Task 3개 + LionProfile을 하나의 트랜잭션으로 처리
    - @transaction.atomic: 중간 오류 발생 시 전체 롤백
    """
    if request.method == "POST":
        name = request.POST.get("name")
        track = request.POST.get("track")

        lion = Lion.objects.create(name=name, track=track)
        Task.objects.create(lion=lion, title="기초 과제")

        # ── 롤백 테스트용 (테스트 시 주석 해제) ──────────────────────────────
        # raise Exception("강제 오류로 롤백 테스트")
        # ──────────────────────────────────────────────────────────────────────

        Task.objects.create(lion=lion, title="중급 과제")
        Task.objects.create(lion=lion, title="심화 과제")
        LionProfile.objects.create(lion=lion)

        return redirect("lion_list")

    # GET: 폼 렌더링
    return render(request, 'lions/new.html', {'track_choices': Lion.TRACK_CHOICES})


def lion_detail(request, pk):
    """아기사자 상세 + 과제 목록 + 프로필 + 태그"""
    lion = get_object_or_404(Lion, pk=pk)

    # 1:N  – Task 전체 / 미완료 / 개수
    tasks = lion.tasks.all()
    incomplete_tasks = lion.tasks.filter(completed=False)
    task_count = lion.tasks.count()

    # 1:1  – LionProfile (없으면 빈 객체)
    profile, _ = LionProfile.objects.get_or_create(lion=lion)

    # N:M  – Lion이 가진 태그 / 추가 가능한 태그
    lion_tags = lion.tags.all()
    all_tags = Tag.objects.all()

    context = {
        'lion': lion,
        'tasks': tasks,
        'incomplete_tasks': incomplete_tasks,
        'task_count': task_count,
        'profile': profile,
        'lion_tags': lion_tags,
        'all_tags': all_tags,
    }
    return render(request, 'lions/lion_detail.html', context)


def lion_edit(request, pk):
    """아기사자 수정"""
    lion = get_object_or_404(Lion, pk=pk)
    if request.method == "POST":
        lion.name = request.POST.get("name")
        lion.track = request.POST.get("track")
        lion.save()
        return redirect("lion_detail", pk=pk)
    return render(request, 'lions/lion_edit.html', {
        'lion': lion,
        'track_choices': Lion.TRACK_CHOICES,
    })


def lion_delete(request, pk):
    """아기사자 삭제 (CASCADE → Task, LionProfile 함께 삭제)"""
    lion = get_object_or_404(Lion, pk=pk)
    if request.method == "POST":
        lion.delete()
        return redirect("lion_list")
    return render(request, 'lions/lion_confirm_delete.html', {'lion': lion})


# ── Task ───────────────────────────────────────────────────────────────────────

def task_toggle(request, pk):
    """과제 완료 상태 토글"""
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect("lion_detail", pk=task.lion.pk)


# ── LionProfile ────────────────────────────────────────────────────────────────

def profile_edit(request, pk):
    """
    프로필 수정
    - get_or_create: 프로필이 없으면 자동 생성, 있으면 조회
    """
    lion = get_object_or_404(Lion, pk=pk)
    profile, created = LionProfile.objects.get_or_create(lion=lion)

    if request.method == "POST":
        profile.github_url = request.POST.get("github_url", "")
        profile.bio = request.POST.get("bio", "")
        profile.save()
        return redirect("lion_detail", pk=pk)

    return render(request, 'lions/profile_edit.html', {'lion': lion, 'profile': profile})


# ── Tag ────────────────────────────────────────────────────────────────────────

def tag_list(request):
    """태그 목록 (N:M 역방향: tag.lions.all())"""
    tags = Tag.objects.prefetch_related('lions').all()
    return render(request, 'lions/tag_list.html', {'tags': tags})


def tag_create(request):
    """태그 생성"""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Tag.objects.get_or_create(name=name)
        return redirect("tag_list")
    return render(request, 'lions/tag_new.html')


def tag_toggle(request, lion_pk, tag_pk):
    """
    Lion ↔ Tag 연결 토글 (N:M)
    - 이미 있으면 remove, 없으면 add
    """
    lion = get_object_or_404(Lion, pk=lion_pk)
    tag = get_object_or_404(Tag, pk=tag_pk)

    if tag in lion.tags.all():
        lion.tags.remove(tag)   # 중간 테이블 DELETE
    else:
        lion.tags.add(tag)      # 중간 테이블 INSERT

    return redirect("lion_detail", pk=lion_pk)
