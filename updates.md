# Update to NeqSim Version 3.x.x from 2.x.x

NeqSim version 3.0 introduces several important updates and changes in both the Java and Python packages, improving usability and simplifying code structure.

### Key Updates

- **Naming Requirement for Process Equipment**:
  All process equipment now requires a unique name upon creation. Previously, objects could be created without a specified name, such as `stream1 = stream(fluid1)`. In version 3, each stream or equipment must have a unique identifier:

  ```python
  stream1 = stream('stream name', fluid1)
  ```

- **Standardized Package Naming**:
  Java package names are now consistently in lowercase. For example, what was previously `thermodynamicOperations` is now `thermodynamicoperations`. This change enhances consistency and aligns with Java package naming conventions.

- **Simplified Package Names**:
  To streamline code and reduce complexity, some package names have been shortened. For instance:
  - `processSimulation` is now `process`
  - `processEquipment` is now `equipment`

These changes are designed to make NeqSim easier to use and align it with modern coding standards. Please update any references to these packages in your projects to ensure compatibility with version 3.
