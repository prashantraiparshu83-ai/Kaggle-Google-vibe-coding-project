import json

# Simulated verified educational databases on our MCP Server
CURRICULUM_DATABASE = {
    "ap physics 1": {
        "title": "AP Physics 1: Algebra-Based Course & Exam Description",
        "description": "Standardized College Board curriculum covering Newtonian Mechanics, Work, Energy, Power, and Rotational Motion.",
        "standards": [
            "Unit 1: Kinematics",
            "Unit 2: Dynamics (Force and Newton's Laws)",
            "Unit 3: Circular Motion and Gravitation",
            "Unit 4: Energy",
            "Unit 5: Momentum",
            "Unit 6: Simple Harmonic Motion",
            "Unit 7: Torque and Rotational Motion"
        ],
        "diagnostics": [
            {
                "id": "app1_q1",
                "question": "A block of mass m is placed on a frictionless ramp inclined at angle θ. What is its acceleration down the ramp?",
                "choices": ["g", "g * sin(θ)", "g * cos(θ)", "g * tan(θ)"],
                "answer": "g * sin(θ)",
                "topic": "Unit 2: Dynamics (Force and Newton's Laws)"
            },
            {
                "id": "app1_q2",
                "question": "A disk of radius R and inertia I rotates about a fixed axis with angular velocity ω. If a second identical disk is dropped onto it, what is the new angular velocity?",
                "choices": ["ω", "ω / 2", "2 * ω", "ω / 4"],
                "answer": "ω / 2",
                "topic": "Unit 7: Torque and Rotational Motion"
            },
            {
                "id": "app1_q3",
                "question": "An object moves in a circular path of radius r at a constant speed v. If the speed is doubled and the radius is halved, by what factor does the centripetal acceleration change?",
                "choices": ["Unchanged", "Doubled", "Quadrupled", "Eightfold"],
                "answer": "Eightfold",
                "topic": "Unit 3: Circular Motion and Gravitation"
            }
        ],
        "resources": {
            "Unit 2: Dynamics (Force and Newton's Laws)": "OpenStax College Physics: Chapter 4 - Dynamics: Force and Newton's Laws of Motion",
            "Unit 7: Torque and Rotational Motion": "Halliday & Resnick: Chapter 10 - Rotation, Section 10.5 - Torque & Angular Momentum",
            "Unit 3: Circular Motion and Gravitation": "OpenStax College Physics: Chapter 6 - Uniform Circular Motion and Gravitation"
        }
    },
    "ap calculus bc": {
        "title": "AP Calculus BC Course & Exam Description",
        "description": "Advanced Placement course covering derivatives, integrals, limits, approximation, sequences, series, and polar/parametric equations.",
        "standards": [
            "Unit 1: Limits and Continuity",
            "Unit 2: Differentiation: Definition and Fundamental Properties",
            "Unit 6: Integration and Accumulation of Change",
            "Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions",
            "Unit 10: Infinite Sequences and Series"
        ],
        "diagnostics": [
            {
                "id": "apc_q1",
                "question": "Determine the limit: lim (x -> 0) of (sin(5x) / x)",
                "choices": ["0", "1", "5", "Does not exist"],
                "answer": "5",
                "topic": "Unit 1: Limits and Continuity"
            },
            {
                "id": "apc_q2",
                "question": "Which of the following is the Taylor series representation of e^x centered at x = 0?",
                "choices": ["Sum of (x^n / n!)", "Sum of ((-1)^n * x^(2n) / (2n)!)", "Sum of (x^n)", "Sum of (n * x^n)"],
                "answer": "Sum of (x^n / n!)",
                "topic": "Unit 10: Infinite Sequences and Series"
            },
            {
                "id": "apc_q3",
                "question": "What is the area of the polar curve r = 3 * sin(θ) for 0 <= θ <= π?",
                "choices": ["9π / 4", "9π / 2", "3π", "9π"],
                "answer": "9π / 4",
                "topic": "Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions"
            }
        ],
        "resources": {
            "Unit 1: Limits and Continuity": "Larson Calculus: Chapter 1 - Limits and Their Properties",
            "Unit 10: Infinite Sequences and Series": "Thomas' Calculus: Chapter 10 - Infinite Sequences and Series, Section 10.8 - Taylor and Maclaurin Series",
            "Unit 9: Parametric Equations, Polar Coordinates, and Vector-Valued Functions": "Larson Calculus: Chapter 10 - Conics, Parametric Equations, and Polar Coordinates"
        }
    },
    "chemistry": {
        "title": "Chemistry Basics & Intermolecular Chemistry Standard",
        "description": "Comprehensive Chemistry standards covering atomic structure, stoichiometry, bonding, and thermochemistry.",
        "standards": [
            "Unit 1: Atoms, Molecules, and Ions",
            "Unit 2: Chemical Bonding & Intermolecular Forces",
            "Unit 3: Chemical Reactions & Stoichiometry"
        ],
        "diagnostics": [
            {
                "id": "chem_q1",
                "question": "What is the molecular geometry of water (H2O)?",
                "choices": ["Linear", "Bent", "Trigonal Planar", "Tetrahedral"],
                "answer": "Bent",
                "topic": "Unit 2: Chemical Bonding & Intermolecular Forces"
            }
        ],
        "resources": {
            "Unit 1: Atoms, Molecules, and Ions": "Brown & LeMay: Chemistry - The Central Science, Chapter 2",
            "Unit 2: Chemical Bonding & Intermolecular Forces": "Brown & LeMay: Chemistry - The Central Science, Chapter 9",
            "Unit 3: Chemical Reactions & Stoichiometry": "Brown & LeMay: Chemistry - The Central Science, Chapter 3"
        }
    },
    "ai": {
        "title": "Artificial Intelligence Foundations",
        "description": "Standardized syllabus covering basic AI paradigms, search algorithms, heuristic functions, and logical representation.",
        "standards": [
            "Unit 1: Introduction to Search Algorithms",
            "Unit 2: Knowledge Representation and Logic",
            "Unit 3: Neural Networks and Deep Learning"
        ],
        "diagnostics": [
            {
                "id": "ai_q1",
                "question": "Which search algorithm is guaranteed to find the shortest path in a graph if edge weights are non-negative?",
                "choices": ["Depth-First Search", "Dijkstra's Algorithm", "Greedy Best-First Search", "Random Walk"],
                "answer": "Dijkstra's Algorithm",
                "topic": "Unit 1: Introduction to Search Algorithms"
            }
        ],
        "resources": {
            "Unit 1: Introduction to Search Algorithms": "Russell & Norvig: Artificial Intelligence: A Modern Approach, Chapter 3",
            "Unit 2: Knowledge Representation and Logic": "Russell & Norvig: Artificial Intelligence: A Modern Approach, Chapter 7",
            "Unit 3: Neural Networks and Deep Learning": "Russell & Norvig: Artificial Intelligence: A Modern Approach, Chapter 21"
        }
    },
    "data science": {
        "title": "Data Science & Applied Statistics Curriculum",
        "description": "Syllabus mapping exploratory data analysis, visualization, mathematical probability, and model metrics.",
        "standards": [
            "Unit 1: Data Cleansing & Exploration",
            "Unit 2: Probability & Statistical Inference",
            "Unit 3: Predictive Modeling & Evaluation"
        ],
        "diagnostics": [
            {
                "id": "ds_q1",
                "question": "Which statistical metric is most sensitive to outliers in a numerical dataset?",
                "choices": ["Median", "Mode", "Mean", "Interquartile Range"],
                "answer": "Mean",
                "topic": "Unit 2: Probability & Statistical Inference"
            }
        ],
        "resources": {
            "Unit 1: Data Cleansing & Exploration": "Python Data Science Handbook: Chapter 3 - Data Manipulation with Pandas",
            "Unit 2: Probability & Statistical Inference": "Python Data Science Handbook: Chapter 4 - Visualization and Statistics",
            "Unit 3: Predictive Modeling & Evaluation": "Python Data Science Handbook: Chapter 5 - Machine Learning foundations"
        }
    },
    "data analyst": {
        "title": "Data Analyst Career Syllabus",
        "description": "Standardized analytical curriculum covering relational database operations, queries, dashboards, and KPI analysis.",
        "standards": [
            "Unit 1: SQL Queries and Data Aggregation",
            "Unit 2: Data Visualization Principles",
            "Unit 3: Business Metrics & Cohort Analysis"
        ],
        "diagnostics": [
            {
                "id": "da_q1",
                "question": "Which SQL clause is used to filter groups returned by a GROUP BY clause?",
                "choices": ["WHERE", "HAVING", "FILTER", "SORT BY"],
                "answer": "HAVING",
                "topic": "Unit 1: SQL Queries and Data Aggregation"
            }
        ],
        "resources": {
            "Unit 1: SQL Queries and Data Aggregation": "SQL for Data Analysis: Chapter 3 - Aggregations and Joins",
            "Unit 2: Data Visualization Principles": "Storytelling with Data: A Data Visualization Guide",
            "Unit 3: Business Metrics & Cohort Analysis": "Lean Analytics: Use Data to Build a Better Startup Faster"
        }
    },
    "web developer": {
        "title": "Web Development Career Roadmap",
        "description": "Foundational web syllabus covering semantic HTML, CSS layout systems, responsive UI design, and JavaScript DOM scripting.",
        "standards": [
            "Unit 1: HTML5 Semantics & CSS Layouts",
            "Unit 2: JavaScript DOM Manipulation & Async API Calls",
            "Unit 3: Web Performance and Client-Side Routing"
        ],
        "diagnostics": [
            {
                "id": "web_q1",
                "question": "What CSS Flexbox property specifies the alignment of items along the main axis?",
                "choices": ["align-items", "justify-content", "align-content", "flex-direction"],
                "answer": "justify-content",
                "topic": "Unit 1: HTML5 Semantics & CSS Layouts"
            }
        ],
        "resources": {
            "Unit 1: HTML5 Semantics & CSS Layouts": "MDN Web Docs: CSS Flexible Box Layout Guide",
            "Unit 2: JavaScript DOM Manipulation & Async API Calls": "Eloquent JavaScript: Chapter 14 - The Document Object Model",
            "Unit 3: Web Performance and Client-Side Routing": "High Performance Browser Networking (Grigorik)"
        }
    },
    "machine learning": {
        "title": "Machine Learning Engineer Curriculum",
        "description": "Professional engineering standard for supervised, unsupervised, and hyperparameter validation frameworks.",
        "standards": [
            "Unit 1: Supervised Learning (Regression & Classification)",
            "Unit 2: Unsupervised Learning (Clustering & Dimensionality Reduction)",
            "Unit 3: Model Tuning & Hyperparameters"
        ],
        "diagnostics": [
            {
                "id": "ml_q1",
                "question": "In a binary classification problem, if the positive class is extremely rare, which evaluation metric is most informative?",
                "choices": ["Accuracy", "F1-Score / Precision-Recall AUC", "Mean Absolute Error", "R-squared"],
                "answer": "F1-Score / Precision-Recall AUC",
                "topic": "Unit 1: Supervised Learning (Regression & Classification)"
            }
        ],
        "resources": {
            "Unit 1: Supervised Learning (Regression & Classification)": "Hands-On Machine Learning (Géron): Chapter 3 - Classification Metrics",
            "Unit 2: Unsupervised Learning (Clustering & Dimensionality Reduction)": "Hands-On Machine Learning (Géron): Chapter 9 - Unsupervised Learning Techniques",
            "Unit 3: Model Tuning & Hyperparameters": "Hands-On Machine Learning (Géron): Chapter 2 - End-to-End Machine Learning Project"
        }
    }
}

class MCPServerConnection:
    """
    Simulated Model Context Protocol (MCP) server interface
    for retrieving academic textbook content, curriculum standards, and verified test item banks.
    """
    def __init__(self, host: str = "mcp://educational-database.local"):
        self.host = host
        self.connected = False

    def connect(self) -> bool:
        """Establish connection to the MCP Server."""
        self.connected = True
        return True

    def get_curriculum(self, subject: str) -> dict:
        """Retrieve standardized curriculum outline for a subject."""
        if not self.connected:
            raise ConnectionError("MCP Server is not connected.")
            
        subj_key = subject.lower().strip()
        if subj_key in CURRICULUM_DATABASE:
            db_entry = CURRICULUM_DATABASE[subj_key]
            return {
                "title": db_entry["title"],
                "description": db_entry["description"],
                "standards": db_entry["standards"]
            }
        else:
            # Return a fallback custom curriculum structure
            return {
                "title": f"Custom Curriculum: {subject.title()}",
                "description": f"Dynamically derived standard for {subject}.",
                "standards": ["Foundations of " + subject, "Intermediate " + subject, "Advanced Concepts in " + subject]
            }

    def get_diagnostic_questions(self, subject: str) -> list:
        """Retrieve verified baseline diagnostic items for a subject."""
        if not self.connected:
            raise ConnectionError("MCP Server is not connected.")
            
        subj_key = subject.lower().strip()
        if subj_key in CURRICULUM_DATABASE:
            return CURRICULUM_DATABASE[subj_key]["diagnostics"]
        else:
            # Fallback diagnostic questions
            return [
                {
                    "id": "cust_q1",
                    "question": f"Explain the fundamental theorem or law of {subject.title()}.",
                    "choices": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "Option A",
                    "topic": f"Foundations of {subject.title()}"
                },
                {
                    "id": "cust_q2",
                    "question": f"What is the primary method of analysis used in {subject.title()}?",
                    "choices": ["Method A", "Method B", "Method C", "Method D"],
                    "answer": "Method A",
                    "topic": f"Intermediate {subject.title()}"
                }
            ]

    def get_textbook_resources(self, subject: str, topic: str) -> str:
        """Fetch verified academic textbook reference for a given topic."""
        if not self.connected:
            raise ConnectionError("MCP Server is not connected.")
            
        subj_key = subject.lower().strip()
        if subj_key in CURRICULUM_DATABASE:
            resources = CURRICULUM_DATABASE[subj_key]["resources"]
            # Find the best match topic
            for k, v in resources.items():
                if k.lower() in topic.lower() or topic.lower() in k.lower():
                    return v
            return f"General textbook reference for {topic} under {subject} curriculum database."
        else:
            return f"Standard academic reference for {topic} in {subject} textbook collection."
