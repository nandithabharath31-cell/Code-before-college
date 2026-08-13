# 🏦 Mini Banking System

A command-line banking application built using **C** to practice core programming concepts by developing a real-world application.

## ✨ Features

* Create and search bank accounts
* Login using account number and PIN
* Check account balance
* Deposit and withdraw money
* Transfer money between accounts
* View transaction history
* Store account data using file handling
* Basic input validation and error handling

## 🧠 Concepts Used

* Variables & Data Types
* Conditions & Loops
* Functions
* Arrays & Strings
* Structures
* Pointers
* Searching
* File Handling
* Input Validation
* Binary files
* fwrite()
* fread()
* Modular programming

## 📁 Project Structure

```text
mini-banking-system/
│
├── src/
│   └── banking.c
│
├── data/
├── README.md
└── .gitignore
```

## 🧠 Program architecture
                    BANKING SYSTEM
                          │
              ┌───────────┴───────────┐
              ↓                       ↓
        Load Accounts            Main Menu
                                      │
                    ┌─────────────────┼────────────────┐
                    ↓                 ↓                ↓
              Create Account        Login             Exit
                                      │
                                      ↓
                              Verify Credentials
                                      │
                                      ↓
                              Logged-in Menu
                                      │             
            ┌─────────────┬───────────┼─────────────┐
            ↓             ↓           ↓             ↓
        Balance        Deposit     Withdraw      Transfer
                                                    │
                                                    ↓
                                             Update accounts
                                                    │
                                                    ↓
                                           Save to file
## 🚧 Status

**Completed ✅**

* [✅] Account creation
* [✅] Duplicate account detection
* [✅] Login system
* [✅] Balance management
* [✅] Deposit & withdrawal
* [✅] Account-to-account transfer
* [✅] changing password
* [✅] File storage(binary file)
* [✅] Basic Input validation
* [✅] Testing & improvements
 
## Limitations

- The program currently expects numeric input for account numbers, PINs,
  menu choices, and transaction amounts.
- Non-numeric input for these fields may cause unexpected behavior.
- This project is intended as a C programming learning project and is not
  designed for real-world banking use.

## Future Improvements

- Add robust input validation for all user inputs.
- Add transaction history and transaction records.
- Add account deletion and account update features.
- Add interest calculation and other banking services.
- Improve security by securely handling PINs instead of storing them directly.
- Add a graphical user interface.
- Improve file/database management using a proper database system.

## 🎯 Goal

To strengthen C programming and problem-solving skills by designing and building a complete application from scratch.

## 👩‍💻 Author

**Nanditha**

Built as part of my C programming learning journey.
