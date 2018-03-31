import os
import praw
import csv
import sys

reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'],
                     password=os.environ['PASSWORD'],
                     user_agent=os.environ['USER_AGENT'],
                     username=os.environ['USERNAME'])

def write_headers():
    with open('archive.csv', 'w', newline='') as csvfile:
        archiver = csv.writer(csvfile)
        archiver.writerow([
            'id',
            'created',
            'created_utc',
            'likes',
            'ups',
            'downs',
            'score',
            'name',
            'subreddit',
            #'num_reports',
            #'num_comments',
            'link_permalink',
            'permalink',
            'approved_at_utc',
            'approved_by',
            'banned_at_utc',
            'banned_by',
            'author',
            'controversiality',
            'body',
        ])

def record_comment_from_archive(comment):
    with open('archive.csv', 'a', newline='') as csvfile:
        archiver = csv.writer(csvfile)
        archiver.writerow(comment)

def record_comment(comment):
    with open('archive.csv', 'a', newline='') as csvfile:
        archiver = csv.writer(csvfile)
        archiver.writerow([
            comment.id,
            comment.created,
            comment.created_utc,
            comment.likes,
            comment.ups,
            comment.downs,
            comment.score,
            comment.name,
            comment.subreddit,
            #comment.num_reports,
            #comment.num_comments,
            comment.link_permalink,
            comment.permalink,
            comment.approved_at_utc,
            comment.approved_by,
            comment.banned_at_utc,
            comment.banned_by,
            comment.author,
            comment.controversiality,
            comment.body.replace('\r', ' ').replace('\n', ' '),
        ])

def read_archive():
    rows = []
    with open('archive.csv', newline='') as csvfile:
        archive_reader = csv.reader(csvfile)
        for row in archive_reader:
            rows.append(row)
    return rows

if __name__ == '__main__':
    try:
        limit = 100
        archive = read_archive()
        del(archive[0]) # remove headers
        last_comment_id = archive[1][0]
    except(FileNotFoundError):
        limit = None
        archive = []
        last_comment_id = None

    write_headers()

    for comment in reddit.redditor(os.environ['REDDITOR']).comments.new(limit=limit):

        if comment.id == last_comment_id:
            for archive_row in archive:
                record_comment_from_archive(archive_row)
            sys.exit(0)
        else:
            record_comment(comment)

        #['approved_at_utc', 'approved_by', 'archived', 'author', 'author_flair_css_class', 'author_flair_text', 'banned_at_utc', 'banned_by', 'block', 'body', 'body_html', 'can_gild', 'can_mod_post', 'clear_vote', 'collapse', 'collapsed', 'collapsed_reason', 'controversiality', 'created', 'created_utc', 'delete', 'disable_inbox_replies', 'distinguished', 'downs', 'downvote', 'edit', 'edited', 'enable_inbox_replies', 'fullname', 'gild', 'gilded', 'id', 'id_from_url', 'is_root', 'is_submitter', 'likes', 'link_author', 'link_id', 'link_permalink', 'link_title', 'link_url', 'mark_read', 'mark_unread', 'mod', 'mod_note', 'mod_reason_by', 'mod_reason_title', 'mod_reports', 'name', 'no_follow', 'num_comments', 'num_reports', 'over_18', 'parent', 'parent_id', 'parse', 'permalink', 'quarantine', 'refresh', 'removal_reason', 'replies', 'reply', 'report', 'report_reasons', 'save', 'saved', 'score', 'score_hidden', 'send_replies', 'stickied', 'submission', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_type', 'uncollapse', 'unsave', 'ups', 'upvote', 'user_reports']
