import enum
import numpy as np
from scipy import sparse
from typing import Sequence
from qib.operator import AbstractOperator, ParticleType, Field


class IFOType(enum.Enum):
    """
    Individual field operator type (e.g., fermionic creation operator).
    """
    BOSON_CREATE  = 1   # bosonic creation operator
    BOSON_ANNIHIL = 2   # bosonic annihilation operator
    FERMI_CREATE  = 3   # fermionic creation operator
    FERMI_ANNIHIL = 4   # fermionic annihilation operator
    MAJORANA_RE   = 5   # "real" Majorana operator
    MAJORANA_IM   = 6   # "imaginary" Majorana operator


class IFODesc:
    """
    Individual field operator description: field and operator type.
    """
    def __init__(self, field: Field, otype: IFOType):
        # consistency checks
        if field.particle_type == ParticleType.QUDIT:
            if (otype != IFOType.BOSON_CREATE) and (otype != IFOType.BOSON_ANNIHIL):
                raise ValueError(f"expecting bosonic operator, but received {otype}")
        elif field.particle_type == ParticleType.FERMION:
            if (otype != IFOType.FERMI_CREATE) and (otype != IFOType.FERMI_ANNIHIL):
                raise ValueError(f"expecting fermionic operator, but received {otype}")
        elif field.particle_type == ParticleType.MAJORANA:
            if (otype != IFOType.MAJORANA_RE) and (otype != IFOType.MAJORANA_IM):
                raise ValueError(f"expecting Majorana operator, but received {otype}")
        self.field = field
        self.otype = otype


class FieldOperatorTerm:
    """
    Field operator term in second quantization, e.g.,
    .. math:: \sum_{j,k} h_{j,k} a^{\dagger}_j a_k

    Each summation index is associated with a field and the
    operator type (e.g., fermionic creation operator).
    """
    def __init__(self, opdesc: Sequence[IFODesc], coeffs):
        self.opdesc = tuple(opdesc)
        self.coeffs = np.array(coeffs, copy=False)
        if self.coeffs.ndim != len(self.opdesc):
            raise ValueError("number of operator descriptions must match dimension of coefficient array")


class FieldOperator(AbstractOperator):
    """
    Field operator in second quantized form.
    """
    def __init__(self, terms: Sequence[FieldOperatorTerm]=[]):
        self.terms = list(terms)

    def fields(self):
        """
        List of all fields appearing in the operator.
        """
        f = set()
        for term in self.terms:
            f = f.union([desc.field for desc in term.opdesc])
        return list(f)

    def as_matrix(self):
        """
        Generate the (sparse) matrix representation of the operator.
        """
        fields = self.fields()
        if len(fields) != 1 or fields[0].ptype != ParticleType.FERMION:
            # currently only a single fermionic field supported
            raise RuntimeError("not implemented yet")
        # number of lattice sites
        L = fields[0].lattice.nsites
        # assemble fermionic creation operators based on Jordan-Wigner transformation
        I = sparse.identity(2)
        Z = sparse.csr_matrix([[ 1.,  0.], [ 0., -1.]])
        U = sparse.csr_matrix([[ 0.,  0.], [ 1.,  0.]])
        clist = []
        for i in range(L):
            c = sparse.identity(1)
            for j in range(L):
                if j < i:
                    c = sparse.kron(Z, c)
                elif j == i:
                    c = sparse.kron(U, c)
                else:
                    c = sparse.kron(I, c)
            clist.append(c)
        # corresponding annihilation operators
        alist = [c.conj().T for c in clist]
        # assemble overall field operator
        op = sparse.csr_matrix((2**L, 2**L))
        for term in self.terms:
            it = np.nditer(term.coeffs, flags=["multi_index"])
            for coeff in it:
                if coeff == 0:
                    continue
                fstring = sparse.identity(2**L)
                for i, j in enumerate(it.multi_index):
                    if term.opdesc[i].otype == IFOType.FERMI_CREATE:
                        fstring = fstring @ clist[j]
                    elif term.opdesc[i].otype == IFOType.FERMI_ANNIHIL:
                        fstring = fstring @ alist[j]
                    else:
                        raise RuntimeError(f"expecting fermionic operator, but received {term.opdesc[i].otype}")
                op += coeff * fstring
        return op