# CPU Simulator
The CPU Simulator simulates how cache, RAM, and SSD works in a computer.  
- [New Discoveries](#discoveries) - New things that I have discovered while building this project!
- [Technologies Used](#technologies) - Frameworks and languages used
- [Installation](#installation) - How to install the CPU Simulator
- [Usage](#usage) - How to use the CPU Simulator
- [Tests](#tests) - How to test the CPU Simulator
- [Contributing](#contributing) - How to contribute in this project
- [License](#license) - Unlicense  

![image](https://github.com/Devbrianhuynh/cpu-simulator/assets/145720981/978fa604-1a7f-4961-a43b-c35c9da7afa8)

## Why did I build this CPU simulator?
- Desire to gain more experience with Python and Flask
- Prepare myself for one, big upcoming project

<a name='discoveries'></a>
## New Discoveries
- Constructor chaining/Inheritance
  - All classes in this entire project are dependent on one another. For example, the Cache class is dependent on the RAM class for the addresses and data if no data could be found in the cache
  - Changes to the SSD, for instance, will affect the RAM, and vice versa
- "global" keyword
   - In order to keep the CPU class the same, I discovered that we can use the keyword "global" to declare that we're using a global variable
   - This saved me lots of time because for each "if" statement in computer(), the CPU class are treated as separate and not related to one another
   - Otherwise, I would have to use PostgreSQL to store data to ensure that the addresses and data remain related
- "super()" function
  - super() saves a space. Instead of calling the same methods over and over for each class, we simply add another class that has the methods we want to this new class; now, this new class will inherit all functions of the old class  

![Inheritance](https://github.com/Devbrianhuynh/cpu-simulator/assets/145720981/ec3a4a7c-ad56-462f-9ea9-fb3cddc7da18)
*example of constructor chaining/inheritence

<a name='technologies'></a>
## Built With
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) - Version 3.0.0
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) - Version 3.12.2
- ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
- ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
- ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
  - Used to help generate code that I had "never seen before" (ex: "global" keyword, super(), etc.)
  - Everything else was built by me

<a name='installation'></a>
## Installation
### Prerequisites
To use the CPU Simulator, you'll need:
- Flask 3.0.0 or later
- Python 3.11.2 or later

### How to Install  
**Install Dependencies**  

1. Flask
   ```bash
   pip install Flask
   ```

**Install CPU Simulator**  

1. Fork this repository, then:

2. To clone and run this software, you'll need Git Bash. From your command line:
    ```bash
    # Clone this repository
    git clone https://github.com/Devbrianhuynh/cpu-simulator
    ```
3. Navigate into the repository
    ```bash
    # Go into the repository
    cd cpu-simulator
    ```
4. Open index.html in a browser
    ```txt
    Open the index.html file in your preferred web browser
    ```

<a name='usage'></a>
## Usage
1. Entering computer specs
   - Enter the model of the CPU, its clock speed, cores, etc.
   - For write policy, there are two choices: Write back OR write through
     - Write back sends data to the RAM only if the cache runs out of space
     - Write through sends data to the RAM alongside with the cache, regardless of how much space there is
2. Writing data
   - Enter a topic (can be anything; ex: food, cars, house, city, country, military, etc.)
   - Write a description, story, or thoughts about that topic. This description will be the data entered into the class
   - Two buttons: Submit and Save
     - Submit sends the data to the cache
     - Save sends the data to the SSD for permanent storage
3. Reading data
   - Enter the topic that you had just entered  































