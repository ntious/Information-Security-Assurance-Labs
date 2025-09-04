Great — thanks for providing the details for **Activity 4**. I’ve turned it into a clean, structured `LAB_INSTRUCTIONS.md` file, consistent with Activities 1–3.

Save as:
`labs/lab4_risk_assessment_qualitative/LAB_INSTRUCTIONS.md`

---

# Lab 4: Threat and Vulnerability Risk Assessment (Qualitative)

## 🎯 Objective

The goal of this lab is to perform a **qualitative risk assessment** by evaluating the **likelihood** and **impact** of each identified threat–vulnerability pair. You will assign an overall risk rating and justify your reasoning for critical risks.

---

## 📖 Background

In **Activity 1**, you created an asset inventory.
In **Activity 2**, you classified assets using **CIA ratings**.
In **Activity 3**, you identified **threats, vulnerabilities, and threat sources**.

Now, in **Activity 4**, you will take the next step in the **risk management process** by assessing the **likelihood and impact** of each threat exploiting a vulnerability. Using a **risk matrix**, you will determine overall risk levels and prioritize risks that need the most urgent attention.

This activity supports the course learning outcomes:
👉 Identify and prioritize threats to information assets
👉 Define an information security strategy and architecture
👉 Plan for risk mitigation and response strategies

---

## 🛠️ Prerequisites

* Completed Excel file from **Activity 3**
* Familiarity with the CIA triad and common cybersecurity risks
* Understanding of qualitative risk assessment concepts

---

## 📝 Tasks

### Step 1 – Open Your File

* Use your group’s Excel file from Activity 3.
* Navigate to the sheet: **`Phase_1_Activity_4`**.

### Step 2 – Assign Likelihood

For each **threat–vulnerability pair**, assign:

* **High** – very probable
* **Medium** – realistically possible
* **Low** – unlikely

### Step 3 – Assign Impact

Assess the potential damage to the asset/organization if realized:

* **High** – severe (legal, financial, reputational loss)
* **Medium** – moderate (service disruption, reputational issues)
* **Low** – limited (minor inconvenience, small cost)

### Step 4 – Determine Risk Rating

Use the **Qualitative Risk Matrix** below to determine the **overall risk rating**.

| Impact ↓ / Likelihood → | Low Likelihood | Medium Likelihood | High Likelihood |
| ----------------------- | -------------- | ----------------- | --------------- |
| **Low Impact**          | Low            | Low               | Medium          |
| **Medium Impact**       | Low            | Medium            | High            |
| **High Impact**         | Medium         | High              | High            |

* 🟢 **Low** → Minimal priority
* 🟡 **Medium** → Needs monitoring
* 🔴 **High** → Requires urgent attention

### Step 5 – Justify High Risks

* For **at least one or two High risks**, provide a short explanation of why they are critical.
* Record justifications in a **separate notes section or sheet**.

### Step 6 – Save and Submit

* Save your file as:

  ```
  GroupNumber_OrganizationName_Phase1_4.xlsx
  ```
* Each student must **submit the same group file individually** before leaving class.

---

## 📂 Deliverables

* Updated Excel file including:

  * Asset ID and Asset Name (from Activity 1)
  * Threat, Vulnerability, Threat Source (from Activity 3)
  * New columns: Likelihood, Impact, Risk Rating
  * Justifications for selected **High** risks

---

## ✅ Evaluation Criteria

* **Consistency** – Likelihood and Impact ratings align with context
* **Correctness** – Risk Rating is derived properly from the matrix
* **Clarity** – Explanations for High risks are specific and realistic
* **Collaboration** – Group work is evident, but each student submits individually

---

## 📘 Learning Outcomes

By completing this lab, you will be able to:

* Evaluate the likelihood of threats exploiting vulnerabilities
* Assess the organizational impact of realized threats
* Assign qualitative risk ratings using a matrix
* Prioritize risks for future mitigation strategies

---

## 📊 Example Table

| Asset ID | Asset Name        | Threat              | Vulnerability            | Threat Source        | Likelihood | Impact | Risk Rating |
| -------- | ----------------- | ------------------- | ------------------------ | -------------------- | ---------- | ------ | ----------- |
| 001      | Customer Database | Data Breach         | Weak password policies   | External attacker    | Medium     | High   | High        |
| 002      | ERP System        | Ransomware Attack   | Lack of software updates | Cybercriminal group  | Medium     | High   | High        |
| 003      | Employee Laptops  | Physical Theft      | No disk encryption       | Insider/Outsider     | High       | Medium | High        |
| 004      | Website           | DDoS Attack         | Insufficient capacity    | Hacktivist group     | Medium     | Medium | Medium      |
| 005      | Financial Records | Unauthorized Access | Poor access controls     | Disgruntled employee | Low        | High   | Medium      |

---

## ⚠️ Ethical Reminder

This exercise is for **educational purposes only**. Always use these methods to strengthen security, not to exploit vulnerabilities.