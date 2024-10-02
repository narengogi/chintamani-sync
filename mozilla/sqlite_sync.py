import sqlite3
import os
from chintamani.utils import create_chintamani_node
from chintamani.endpoints import insert_child
class SQLiteSync:
    def __init__(self):
        self.conn = sqlite3.connect(os.getenv('MOZILLA_BROWSING_HISTORY_SQLITE_PATH'))
        self.conn.row_factory = sqlite3.Row 

    def exit(self):
        self.conn.close()

    def _create_origin_node(self, row):
        node = {
            'host': row['prefix'] + row['host'],
            'frecency': row['frecency'],
        }
        chintamani_node = create_chintamani_node(node, 'host')
        return chintamani_node

    def _create_place_node(self, row, metadata_row, referrer_row):
        node = {
            'url': row['url'],
            'visit_count': row['visit_count'],
            'title': row['title'],
            'last_visit_date': row['last_visit_date'],
            'description': row['description'],
            'preview_image_url': row['preview_image_url'],
            'icon_url': row['preview_image_url'],
            'last_visit': row['last_visit_date'],
        }
        if (metadata_row):
            node['first_visit'] = metadata_row['created_at']
            node['view_time_in_seconds'] = metadata_row['total_view_time']
            node['typing_time_in_seconds'] = metadata_row['typing_time']
            node['key_presses'] = metadata_row['key_presses']
            node['scrolling_time_in_seconds'] = metadata_row['scrolling_time']
            node['scrolling_distance'] = metadata_row['scrolling_distance']
        if (referrer_row):
            node['referrer_url'] = referrer_row['url']
        chintamani_node = create_chintamani_node(node, 'url')
        return chintamani_node
    
    def _create_bookmark_node(self, row):
        node = {
            'url': row['url'],
            'title': row['title'],
            'description': row['description'],
            'favicon_url': row['favicon_url'],
            'icon_url': row['preview_image_url'],
        }
        

    def sync_origins(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM moz_origins")
        while True:
            rows = cursor.fetchmany(size=10)
            if not rows:
                break
            for row in rows:
                node = self._create_origin_node(row)
                print('inserting origin', node)
                insert_child(child_label="ORIGIN", child_json=node, parent_path="FIREFOX.ORIGINS", relationship="ORIGIN")
                self.sync_places(node, row['id'])
                print('inserted origin')
        cursor.close()

    def sync_places(self, parent_node, origin_id):
        cursor = self.conn.cursor()
        second_cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM moz_places WHERE origin_id = ?", (origin_id,))
        while True:
            rows = cursor.fetchmany(size=10)
            if not rows:
                break
            for row in rows:
                metadata_row = second_cursor.execute("SELECT * FROM moz_places_metadata WHERE place_id = ?", (row['id'],)).fetchone()
                referrer_row = second_cursor.execute("SELECT * FROM moz_places WHERE id = ?", (metadata_row['referrer_place_id'],)).fetchone() if metadata_row else {}
                node = self._create_place_node(row=row, metadata_row=metadata_row or {}, referrer_row=referrer_row or {})
                print('inserting place', node)
                insert_child(child_label="PLACE", child_json=node, parent_path="FIREFOX.ORIGINS.ORIGIN", parent_title=parent_node['title'], relationship="PLACE")
                print('inserted place')
        cursor.close()

    # def sync_bookmarks(self)
    #     cursor = self.conn.cursor()
    #     second_cursor = self.conn.cursor()
    #     cursor.execute("SELECT * FROM moz_bookmarks")
    #     while True:
    #         rows = cursor.fetchmany(size=10)
    #         if not rows:
    #             break
    #         for row in rows:
                
    #             node = self._create_bookmark_node(row)
    #             print('inserting bookmark', node)
    #             insert_child(child_label="BOOKMARK", child_json=node, parent_path="FIREFOX.BOOKMARKS", relationship="BOOKMARK")
    #             print('inserted bookmark')
    #     cursor.close()