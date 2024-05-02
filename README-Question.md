# Full Stack Development

This mini project will test your full stack software engineering skills. Please push your code to this GitLab repo within 7 days of starting the test.

#### Rules

- Complete the challenge(s) on your own.
- Referencing of online resources is expected.
- All code, markup, and assets should be pushed to the provided repository.
- You are encouraged to ask us questions at any point.
- Note any deviations from the specification.
- You may use any supporting library you deem appropriate.

### Backend Development

1.  Set up a Python project in be/
2.  Create a Postgres relational database with a schema for the following data structure:

- A spacecraft (root node) is built from a tree of nodes. Each node has a name. The path of a node can be inferred from the name hierarchy (e.g. _'/root/parent/child'_).
- Each node can have any number of properties. A property is a key value pair, where the key is a string and the value is a decimal number.

3.  Develop a way to interact with this database. You may use an ORM of your own choice.
4.  Seed the database with the following structure (entries with values are properties, others are nodes):

- Spacecraft
  - Name: "Intrepid"
  - Mass: 124.00
  - Bus
    - Thruster1
      - Thrust: 9.493
      - ISP: 12.156
    - Thruster2
      - Thrust: 9.413
      - ISP: 11.632
    - Thruster3
      - Thrust: 9.899
      - ISP: 12.551
  - Payload
    - DarkMatterCamera
      - Exposure: 1.622
      - Sensitivity: 15.110

5.  Expose HTTP endpoints for the following operations:

    1.  Create a node with a specified parent
    2.  Add a property on a specific node
    3.  Return the subtree of nodes with their properties for a provided node path

6.  Create unit tests for endpoint **3** above.

### Frontend Development

1.  Create a new Angular CLI project in fe/
2.  Make 2 new components 

- **Component A**
  - Retrieve data from the backend app you made in the prior task
  - It should have an input box to enter a node path
  - On each keypress the component should query the backend for a subtree matching that path. Inflight requests should be canceled for new ones.
  - Use Component B to render the returned subtree
- **Component B**
  - Should render a single node tree and all properties
  - The label of a property should be GREEN if the value is greater than 10

3.  Use Angular Material for the following

- Use the Dialog component to make a reusable "Confirm" box
- Use the above component to make a delete button with confirmation for each node (this does not need to be connected to the backend)

4.  Create a Pipe

- This pipe should render how long ago it was since this item was created (e.g _'created 1 hour ago'_)
- Implement this pipe onto each item in the displayed tree

5.  Create a unit test to assert that the colour of the Component B label behaves as specified

### Deployment

1.  Create a Docker Compose file to locally deploy the database, backend and frontend.
