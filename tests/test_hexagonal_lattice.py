import numpy as np
import unittest
import qib


class TestHexagonalLattice(unittest.TestCase):

    def test_lattice_adjacency_with_delete(self):
        """
        Test construction of adjacency matrices.
        Delete option enabled.
        """
        for Lx in range(1, 5):
            for Ly in range(1, 5):
                # two-dimensional lattice, open boundary conditions, COLS_SHIFTED_UP convention
                latt = qib.lattice.HexagonalLattice((Lx, Ly), pbc=False, convention=qib.lattice.HexagonalLatticeConvention.COLS_SHIFTED_UP)
                self.assertEqual(latt.ndim, 2)
                self.assertEqual(latt.nsites, 2*Lx*Ly +2*(Lx+Ly))
                adj = latt.adjacency_matrix()
                self.assertTrue(np.array_equal(adj, adj.T))
                if Ly>1:
                    nrows_square = 2*Lx+2
                    self.assertEqual(latt.nsites, latt.nsites_square-2)
                else:
                    nrows_square = 2*Lx+1
                    self.assertEqual(latt.nsites, latt.nsites_square)
                ncols_square = Ly+1
                self.assertEqual(latt.shape_square, (nrows_square,ncols_square))
                enum_latt = [(x, y) for x in range(nrows_square) for y in range(ncols_square)]
                adj_ref = np.zeros((len(enum_latt), len(enum_latt)), dtype=int)
                for i, a in enumerate(enum_latt):
                    for j, b in enumerate(enum_latt):
                        if a[1] == b[1] and abs(a[0]-b[0]) == 1:
                            adj_ref[i, j] = 1
                        elif a[0] == b[0] and abs(a[1]-b[1])==1:
                            if (max(a[1],b[1])+a[0])%2 == 1:
                                adj_ref[i,j] = 1
                # delete extra points
                if Ly > 1:
                    adj_ref = np.delete(adj_ref, (2*Lx+1)*(Ly+1), 0)
                    adj_ref = np.delete(adj_ref, (2*Lx+1)*(Ly+1), 1)
                    if Ly%2 == 1:
                        adj_ref= np.delete(adj_ref, -1, 0)
                        adj_ref= np.delete(adj_ref, -1, 1)
                    else:
                        adj_ref = np.delete(adj_ref, Ly, 0)
                        adj_ref = np.delete(adj_ref, Ly, 1)
                self.assertTrue(np.array_equal(adj, adj_ref))

                # two-dimensional lattice, open boundary conditions ROWS_SHIFTED_LEFT convention
                latt = qib.lattice.HexagonalLattice((Lx, Ly), pbc=False, convention=qib.lattice.HexagonalLatticeConvention.ROWS_SHIFTED_LEFT)
                self.assertEqual(latt.ndim, 2)
                self.assertEqual(latt.nsites, 2*Lx*Ly +2*(Lx+Ly))
                adj = latt.adjacency_matrix()
                self.assertTrue(np.array_equal(adj, adj.T))
                if Lx>1:
                    ncols_square = 2*Ly+2
                    self.assertEqual(latt.nsites, latt.nsites_square-2)
                else:
                    ncols_square = 2*Ly+1
                    self.assertEqual(latt.nsites, latt.nsites_square)
                nrows_square = Lx+1
                self.assertEqual(latt.shape_square, (nrows_square,ncols_square))
                enum_latt = [(x, y) for x in range(nrows_square) for y in range(ncols_square)]
                adj_ref = np.zeros((len(enum_latt), len(enum_latt)), dtype=int)
                for i, a in enumerate(enum_latt):
                    for j, b in enumerate(enum_latt):
                        if a[0] == b[0] and abs(a[1]-b[1]) == 1:
                            adj_ref[i, j] = 1
                        elif a[1] == b[1] and abs(a[0]-b[0])==1:
                            if (max(a[0],b[0])+a[1])%2 == 1 :
                                adj_ref[i,j] = 1
                # delete extra points        
                if Lx > 1:
                    adj_ref = np.delete(adj_ref, 2*Ly+1, 0)
                    adj_ref = np.delete(adj_ref, 2*Ly+1, 1)
                    if Lx%2 == 1:
                        adj_ref = np.delete(adj_ref, -1, 0)
                        adj_ref = np.delete(adj_ref, -1, 1)
                    else:
                        adj_ref = np.delete(adj_ref, Lx*(2*Ly+2)-1, 0)
                        adj_ref = np.delete(adj_ref, Lx*(2*Ly+2)-1, 1)
                self.assertTrue(np.array_equal(adj, adj_ref))
    
    def test_lattice_adjacency_without_delete(self):
        """
        Test construction of adjacency matrices.
        Delete option unenabled.
        """
        for Lx in range(1, 5):
            for Ly in range(1, 5):
                # two-dimensional lattice, open boundary conditions, COLS_SHIFTED_UP convention
                latt = qib.lattice.HexagonalLattice((Lx, Ly), pbc=False, convention=qib.lattice.HexagonalLatticeConvention.COLS_SHIFTED_UP)
                self.assertEqual(latt.ndim, 2)
                self.assertEqual(latt.nsites, 2*Lx*Ly +2*(Lx+Ly))
                adj = latt.adjacency_matrix(delete=False)
                self.assertTrue(np.array_equal(adj, adj.T))
                if Ly>1:
                    nrows_square = 2*Lx+2
                    self.assertEqual(latt.nsites, latt.nsites_square-2)
                else:
                    nrows_square = 2*Lx+1
                    self.assertEqual(latt.nsites, latt.nsites_square)
                ncols_square = Ly+1
                self.assertEqual(latt.shape_square, (nrows_square,ncols_square))
                enum_latt = [(x, y) for x in range(nrows_square) for y in range(ncols_square)]
                adj_ref = np.zeros((len(enum_latt), len(enum_latt)), dtype=int)
                for i, a in enumerate(enum_latt):
                    for j, b in enumerate(enum_latt):
                        if a[1] == b[1] and abs(a[0]-b[0]) == 1:
                            adj_ref[i, j] = 1
                        elif a[0] == b[0] and abs(a[1]-b[1])==1:
                            if (max(a[1],b[1])+a[0])%2 == 1:
                                adj_ref[i,j] = 1
                # disconnect extra points
                if Ly > 1:
                    adj_ref[(2*Lx+1)*(Ly+1), :] = 0
                    adj_ref[:, (2*Lx+1)*(Ly+1)] = 0
                    if Ly%2 == 1:
                        adj_ref[-1, :] = 0
                        adj_ref[:, -1] = 0
                    else:
                        adj_ref[Ly, :] = 0
                        adj_ref[:, Ly] = 0
                self.assertTrue(np.array_equal(adj, adj_ref))

                # two-dimensional lattice, open boundary conditions ROWS_SHIFTED_LEFT convention
                latt = qib.lattice.HexagonalLattice((Lx, Ly), pbc=False, convention=qib.lattice.HexagonalLatticeConvention.ROWS_SHIFTED_LEFT)
                self.assertEqual(latt.ndim, 2)
                self.assertEqual(latt.nsites, 2*Lx*Ly +2*(Lx+Ly))
                adj = latt.adjacency_matrix(delete=False)
                self.assertTrue(np.array_equal(adj, adj.T))
                if Lx>1:
                    ncols_square = 2*Ly+2
                    self.assertEqual(latt.nsites, latt.nsites_square-2)
                else:
                    ncols_square = 2*Ly+1
                    self.assertEqual(latt.nsites, latt.nsites_square)
                nrows_square = Lx+1
                self.assertEqual(latt.shape_square, (nrows_square,ncols_square))
                enum_latt = [(x, y) for x in range(nrows_square) for y in range(ncols_square)]
                adj_ref = np.zeros((len(enum_latt), len(enum_latt)), dtype=int)
                for i, a in enumerate(enum_latt):
                    for j, b in enumerate(enum_latt):
                        if a[0] == b[0] and abs(a[1]-b[1]) == 1:
                            adj_ref[i, j] = 1
                        elif a[1] == b[1] and abs(a[0]-b[0])==1:
                            if (max(a[0],b[0])+a[1])%2 == 1 :
                                adj_ref[i,j] = 1
                # delete extra points        
                if Lx > 1:
                    adj_ref[2*Ly+1, :] = 0
                    adj_ref[:, 2*Ly+1] = 0
                    if Lx%2 == 1:
                        adj_ref[-1, :] = 0
                        adj_ref[:, -1] = 0
                    else:
                        adj_ref[Lx*(2*Ly+2), :] = 0
                        adj_ref[:, Lx*(2*Ly+2)] = 0
                self.assertTrue(np.array_equal(adj, adj_ref))

    def test_lattice_coords(self):
        """
        Test lattice coordinate indexing.
        """
        # two-dimensional lattice, open boundary conditions
        for Lx in range(1, 5):
            for Ly in range(1, 5):
                #print(Lx,Ly)
                latt = qib.lattice.HexagonalLattice((Lx, Ly), pbc=False, convention=qib.lattice.HexagonalLatticeConvention.COLS_SHIFTED_UP)
                for i in range(latt.nsites):
                    self.assertEqual(i, latt.coord_to_index(latt.index_to_coord(i)))
                    self.assertEqual(i, latt.coord_to_index(latt.index_to_coord(i, delete=False), delete=False))
                latt = qib.lattice.HexagonalLattice((Lx, Ly), pbc=False, convention=qib.lattice.HexagonalLatticeConvention.ROWS_SHIFTED_LEFT)
                for i in range(latt.nsites):
                    self.assertEqual(i, latt.coord_to_index(latt.index_to_coord(i)))
                    self.assertEqual(i, latt.coord_to_index(latt.index_to_coord(i, delete=False), delete=False))
                    
if __name__ == "__main__":
    unittest.main()
