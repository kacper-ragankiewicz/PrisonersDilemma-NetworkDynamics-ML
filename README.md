# Axelrod-Based Strategy Implementation

We base our work on the **Axelrod** library.

Example: [AxelrodExamples](https://github.com/Axelrod-Python/AxelrodExamples)

## Assumptions
Implementation of strategies for a Facebook friends network.

### Version 1 (11.01.2025):
1. Strategies do not influence relationships between users.
2. Users do not establish new relationships.

---

## To Do
- [x] **Generate the graph of relationships from Facebook**
      - Same graph as described in **complex systems problem_5.pdf**.
- [x] **Plot the MTX from Facebook**
- [ ] **Filter the MTX**
- [x] **Assign strategies**  
      Selected strategies (10):
   1. **Cooperator**
   2. **Defector**
   3. **Tit For Tat**
   4. **Grudger**
   5. **Random**
   6. **Pavlovian Strategy**
   7. **Imitate the Best from Friend List**

   **Memory-based strategies**:
   8. **Zero Determinant Strategy - Extortion**
   9. **Cappri Strategy**
   10. **Appeaser Strategy**

- [x] **Run the simulation for T iterations**
- [x] **Enable strategy switching**
