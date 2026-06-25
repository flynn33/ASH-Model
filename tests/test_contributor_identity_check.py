from scripts.github.check_contributor_identities import (
    CommitMetadata,
    RESTRICTED_EMAILS,
    RESTRICTED_NAMES,
    is_restricted_identity,
    restricted_coauthor_line,
    scan_commit,
)


def test_restricted_author_names_and_emails_are_detected():
    assert is_restricted_identity(next(iter(RESTRICTED_NAMES)), "owner@example.com")
    assert is_restricted_identity("Project Owner", next(iter(RESTRICTED_EMAILS)))


def test_regular_owner_identity_is_allowed():
    assert not is_restricted_identity(
        "flynn33", "94642455+flynn33@users.noreply.github.com"
    )


def test_restricted_coauthor_trailer_is_detected():
    email = next(iter(RESTRICTED_EMAILS))
    assert restricted_coauthor_line(f"Co-authored-by: Restricted <{email}>")


def test_scan_commit_reports_restricted_author_and_committer():
    metadata = CommitMetadata(
        commit="abc123",
        author_name=next(iter(RESTRICTED_NAMES)),
        author_email="owner@example.com",
        committer_name="Project Owner",
        committer_email=next(iter(RESTRICTED_EMAILS)),
        message="Update repository policy",
    )

    assert [violation.field for violation in scan_commit(metadata)] == [
        "author",
        "committer",
    ]


def test_scan_commit_accepts_owner_metadata():
    metadata = CommitMetadata(
        commit="abc123",
        author_name="flynn33",
        author_email="94642455+flynn33@users.noreply.github.com",
        committer_name="GitHub",
        committer_email="noreply@github.com",
        message="Update repository policy",
    )

    assert scan_commit(metadata) == []
