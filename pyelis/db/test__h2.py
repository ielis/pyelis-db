import unittest

from pkg_resources import resource_filename

from .h2 import H2DbManager


class TestH2DbManager(unittest.TestCase):

    def setUp(self) -> None:
        self._db_path = resource_filename(__name__, "test_data/hg19_sv_database.mv.db")

    def test_java_is_installed_in_system(self):
        self.assertTrue(H2DbManager.check_java_is_in_system())

    def test_split_db_path_works(self):
        folder, dbfile = H2DbManager.split_db_path(self._db_path)
        self.assertTrue(folder.endswith("test_data"))
        self.assertEqual("hg19_sv_database", dbfile)

    def test_fetch_some_data(self):
        with H2DbManager(self._db_path, "sa", "sa") as h2:
            with h2.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('select * from PBGA.CLINGEN_TRIPLOSENSITIVITY order by START, END')
                    actual = tuple([x for i, x in zip(range(5), cur.fetchall())])
                    expected = ((10, 180405, 300577, 'ZMYND11', 'NO_EVIDENCE'),
                                (7, 192969, 300740, 'FAM20C', 'UNKNOWN'),
                                (9, 214865, 465259, 'DOCK8', 'UNKNOWN'),
                                (16, 222846, 223709, 'HBA2', 'NO_EVIDENCE'),
                                (16, 226650, 227521, 'HBA1', 'NO_EVIDENCE'))
        self.assertTupleEqual(expected, actual)

    def test_works_with_unknown_h2_version(self):
        # works with default version
        with H2DbManager(self._db_path, "sa", "sa", h2_version='unknown') as h2:
            with h2.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('select * from PBGA.CLINGEN_TRIPLOSENSITIVITY order by START, END limit 2')
                    actual = tuple(cur.fetchall())

        self.assertTupleEqual(((10, 180405, 300577, 'ZMYND11', 'NO_EVIDENCE'),
                               (7, 192969, 300740, 'FAM20C', 'UNKNOWN')), actual)
