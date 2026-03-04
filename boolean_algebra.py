#!/usr/bin/env python3
"""
Boolean Algebra Library
Implements logic gates, truth tables, and Boolean operations
Based on fundamental logic principles
"""

class BooleanAlgebra:
    """Boolean algebra operations and laws"""
    
    # Basic Logic Gates
    @staticmethod
    def AND(a, b):
        """Logical AND: True only if both inputs are True"""
        return a and b
    
    @staticmethod
    def OR(a, b):
        """Logical OR: True if at least one input is True"""
        return a or b
    
    @staticmethod
    def NOT(a):
        """Logical NOT: Inverts the input"""
        return not a
    
    @staticmethod
    def NAND(a, b):
        """NAND: NOT AND - Universal gate"""
        return not (a and b)
    
    @staticmethod
    def NOR(a, b):
        """NOR: NOT OR - Universal gate"""
        return not (a or b)
    
    @staticmethod
    def XOR(a, b):
        """XOR: Exclusive OR - True if inputs differ"""
        return a != b
    
    @staticmethod
    def XNOR(a, b):
        """XNOR: Exclusive NOR - True if inputs are same"""
        return a == b
    
    # Derived Operations
    @staticmethod
    def IMPLIES(a, b):
        """Logical implication: A → B"""
        return (not a) or b
    
    @staticmethod
    def IFF(a, b):
        """If and only if: A ↔ B (biconditional)"""
        return a == b
    
    # Boolean Laws
    @staticmethod
    def identity_law(a):
        """Identity: A AND 1 = A, A OR 0 = A"""
        return {
            'AND_identity': BooleanAlgebra.AND(a, True) == a,
            'OR_identity': BooleanAlgebra.OR(a, False) == a
        }
    
    @staticmethod
    def null_law(a):
        """Null: A AND 0 = 0, A OR 1 = 1"""
        return {
            'AND_null': BooleanAlgebra.AND(a, False) == False,
            'OR_null': BooleanAlgebra.OR(a, True) == True
        }
    
    @staticmethod
    def idempotent_law(a):
        """Idempotent: A AND A = A, A OR A = A"""
        return {
            'AND_idempotent': BooleanAlgebra.AND(a, a) == a,
            'OR_idempotent': BooleanAlgebra.OR(a, a) == a
        }
    
    @staticmethod
    def complement_law(a):
        """Complement: A AND NOT A = 0, A OR NOT A = 1"""
        return {
            'AND_complement': BooleanAlgebra.AND(a, not a) == False,
            'OR_complement': BooleanAlgebra.OR(a, not a) == True
        }
    
    @staticmethod
    def double_negation(a):
        """Double Negation: NOT(NOT A) = A"""
        return BooleanAlgebra.NOT(BooleanAlgebra.NOT(a)) == a
    
    @staticmethod
    def commutative_law(a, b):
        """Commutative: A AND B = B AND A, A OR B = B OR A"""
        return {
            'AND_commutative': BooleanAlgebra.AND(a, b) == BooleanAlgebra.AND(b, a),
            'OR_commutative': BooleanAlgebra.OR(a, b) == BooleanAlgebra.OR(b, a)
        }
    
    @staticmethod
    def associative_law(a, b, c):
        """Associative: (A AND B) AND C = A AND (B AND C)"""
        return {
            'AND_associative': BooleanAlgebra.AND(BooleanAlgebra.AND(a, b), c) == 
                              BooleanAlgebra.AND(a, BooleanAlgebra.AND(b, c)),
            'OR_associative': BooleanAlgebra.OR(BooleanAlgebra.OR(a, b), c) == 
                             BooleanAlgebra.OR(a, BooleanAlgebra.OR(b, c))
        }
    
    @staticmethod
    def distributive_law(a, b, c):
        """Distributive: A AND (B OR C) = (A AND B) OR (A AND C)"""
        left = BooleanAlgebra.AND(a, BooleanAlgebra.OR(b, c))
        right = BooleanAlgebra.OR(BooleanAlgebra.AND(a, b), BooleanAlgebra.AND(a, c))
        return left == right
    
    @staticmethod
    def de_morgan_law(a, b):
        """De Morgan's Laws: NOT(A AND B) = NOT A OR NOT B"""
        return {
            'de_morgan_and': BooleanAlgebra.NOT(BooleanAlgebra.AND(a, b)) == 
                            BooleanAlgebra.OR(BooleanAlgebra.NOT(a), BooleanAlgebra.NOT(b)),
            'de_morgan_or': BooleanAlgebra.NOT(BooleanAlgebra.OR(a, b)) == 
                           BooleanAlgebra.AND(BooleanAlgebra.NOT(a), BooleanAlgebra.NOT(b))
        }
    
    @staticmethod
    def absorption_law(a, b):
        """Absorption: A OR (A AND B) = A"""
        return {
            'absorption_1': BooleanAlgebra.OR(a, BooleanAlgebra.AND(a, b)) == a,
            'absorption_2': BooleanAlgebra.AND(a, BooleanAlgebra.OR(a, b)) == a
        }
    
    @staticmethod
    def truth_table(operation, num_inputs=2):
        """Generate truth table for a Boolean operation"""
        if num_inputs == 1:
            print(f"\nTruth Table for {operation.__name__}:")
            print("A | Output")
            print("--|-------")
            for a in [False, True]:
                result = operation(a)
                print(f"{int(a)} | {int(result)}")
        elif num_inputs == 2:
            print(f"\nTruth Table for {operation.__name__}:")
            print("A | B | Output")
            print("--|---|-------")
            for a in [False, True]:
                for b in [False, True]:
                    result = operation(a, b)
                    print(f"{int(a)} | {int(b)} | {int(result)}")
        elif num_inputs == 3:
            print(f"\nTruth Table for {operation.__name__}:")
            print("A | B | C | Output")
            print("--|---|---|-------")
            for a in [False, True]:
                for b in [False, True]:
                    for c in [False, True]:
                        result = operation(a, b, c)
                        print(f"{int(a)} | {int(b)} | {int(c)} | {int(result)}")


def main():
    """Demonstrate Boolean algebra operations"""
    ba = BooleanAlgebra()
    
    print("=" * 50)
    print("BOOLEAN ALGEBRA LIBRARY")
    print("=" * 50)
    
    # Truth tables for basic gates
    ba.truth_table(ba.AND)
    ba.truth_table(ba.OR)
    ba.truth_table(ba.NOT, num_inputs=1)
    ba.truth_table(ba.XOR)
    ba.truth_table(ba.NAND)
    ba.truth_table(ba.NOR)
    
    # Verify Boolean laws
    print("\n" + "=" * 50)
    print("BOOLEAN LAWS VERIFICATION")
    print("=" * 50)
    
    test_values = [(False, False), (False, True), (True, False), (True, True)]
    
    print("\nCommutative Law:")
    for a, b in test_values:
        result = ba.commutative_law(a, b)
        print(f"  A={int(a)}, B={int(b)}: {result}")
    
    print("\nDe Morgan's Laws:")
    for a, b in test_values:
        result = ba.de_morgan_law(a, b)
        print(f"  A={int(a)}, B={int(b)}: {result}")
    
    print("\nDistributive Law:")
    for a in [False, True]:
        for b in [False, True]:
            for c in [False, True]:
                result = ba.distributive_law(a, b, c)
                print(f"  A={int(a)}, B={int(b)}, C={int(c)}: {result}")


if __name__ == '__main__':
    main()
