#include <iostream>
#include <string>

using namespace std;

// This file has two small demos:
// 1. basic OOP ideas
// 2. SOLID principles

// -----------------------------
// 1) Basic OOP principles
// -----------------------------
// Encapsulation means keeping data inside the class and only allowing safe access.
class BankAccount {
    double balance_; // private by default because this is a class

public:
    // explicit stops C++ from turning a plain number into a BankAccount automatically.
    explicit BankAccount(double initialBalance) : balance_(initialBalance) {}

    void deposit(double amount) {
        if (amount > 0) {
            balance_ += amount;
        }
    }

    void withdraw(double amount) {
        if (amount > 0 && amount <= balance_) {
            balance_ -= amount;
        }
    }

    // const here means this function will not change the object.
    double balance() const {
        return balance_;
    }
};

// Abstraction means we show what something can do, not how it does it.
class Shape {
public:
    // virtual means this function can be replaced in child classes.
    // A virtual destructor is important when deleting a child object through a base pointer.
    virtual ~Shape() = default;

    // = 0 means the child classes must implement these functions.
    virtual string name() const = 0;
    virtual double area() const = 0;
};

// Inheritance means Circle is a Shape.
class Circle : public Shape {
    double radius_;

public:
    explicit Circle(double radius) : radius_(radius) {}

    // const means no object data is changed.
    // override means this is intentionally replacing a base-class virtual function.
    string name() const override {
        return "Circle";
    }

    double area() const override {
        return 3.14159 * radius_ * radius_;
    }
};

class Rectangle : public Shape {
    double width_;
    double height_;

public:
    Rectangle(double width, double height) : width_(width), height_(height) {}

    string name() const override {
        return "Rectangle";
    }

    double area() const override {
        return width_ * height_;
    }
};

// Polymorphism means the same function works with different child objects.
void showShapeInfo(const Shape& shape) {
    cout << shape.name() << " area = " << shape.area() << '\n';
}

void basicOopDemo() {
    cout << "Basic OOP demo:\n";

    BankAccount account(1000.0);
    account.deposit(250.0);
    account.withdraw(100.0);
    cout << "Account balance: " << account.balance() << '\n';

    Circle circle(5.0);
    Rectangle rectangle(4.0, 6.0);

    showShapeInfo(circle);
    showShapeInfo(rectangle);

    cout << '\n';
}

// -----------------------------
// 2) SOLID principles
// -----------------------------
//
// SRP: Single Responsibility Principle
// A class should have one main job.
class Invoice {
    string item_;
    double price_;

public:
    Invoice(const string& item, double price) : item_(item), price_(price) {}

    string item() const {
        return item_;
    }

    double price() const {
        return price_;
    }
};

// This class only prints invoices.
class InvoicePrinter {
public:
    void print(const Invoice& invoice) const {
        cout << "Invoice: " << invoice.item() << ", price = " << invoice.price() << '\n';
    }
};

// OCP: Open/Closed Principle
// Add new behavior by creating new classes, not by rewriting old code.
class IDiscountPolicy {
public:
    virtual ~IDiscountPolicy() = default;
    virtual double discount(double price) const = 0;
};

class NoDiscount : public IDiscountPolicy {
public:
    double discount(double) const override {
        return 0.0;
    }
};

class StudentDiscount : public IDiscountPolicy {
public:
    double discount(double price) const override {
        return price * 0.10;
    }
};

double finalPrice(double price, const IDiscountPolicy& discountPolicy) {
    return price - discountPolicy.discount(price);
}

// LSP: Liskov Substitution Principle
// If a child class inherits from a base class, it should still behave correctly.
class PaymentMethod {
public:
    virtual ~PaymentMethod() = default;
    virtual void pay(double amount) const = 0;
};

class CashPayment : public PaymentMethod {
public:
    void pay(double amount) const override {
        cout << "Paid " << amount << " in cash\n";
    }
};

class CardPayment : public PaymentMethod {
public:
    void pay(double amount) const override {
        cout << "Paid " << amount << " by card\n";
    }
};

void processPayment(const PaymentMethod& paymentMethod, double amount) {
    paymentMethod.pay(amount);
}

// ISP: Interface Segregation Principle
// Keep interfaces small so classes only implement what they need.
class IPrinter {
public:
    virtual ~IPrinter() = default;
    virtual void print(const string& document) const = 0;
};

class IScanner {
public:
    virtual ~IScanner() = default;
    virtual void scan(const string& document) const = 0;
};

class SimplePrinter : public IPrinter {
public:
    void print(const string& document) const override {
        cout << "Printing: " << document << '\n';
    }
};

class AllInOneMachine : public IPrinter, public IScanner {
public:
    void print(const string& document) const override {
        cout << "Printing: " << document << '\n';
    }

    void scan(const string& document) const override {
        cout << "Scanning: " << document << '\n';
    }
};

void printDocument(const IPrinter& printer, const string& document) {
    printer.print(document);
}

void scanDocument(const IScanner& scanner, const string& document) {
    scanner.scan(document);
}

// DIP: Dependency Inversion Principle
// High-level code should depend on an abstraction, not one concrete class.
class IPaymentGateway {
public:
    virtual ~IPaymentGateway() = default;
    virtual void charge(double amount) const = 0;
};

class ConsolePaymentGateway : public IPaymentGateway {
public:
    void charge(double amount) const override {
        cout << "Charging payment gateway for " << amount << '\n';
    }
};

class CheckoutService {
    const IPaymentGateway& gateway_;

public:
    explicit CheckoutService(const IPaymentGateway& gateway) : gateway_(gateway) {}

    void checkout(double amount) const {
        gateway_.charge(amount);
    }
};

void solidDemo() {
    cout << "SOLID demo:\n";

    Invoice invoice("Notebook", 500.0);
    InvoicePrinter printer;
    printer.print(invoice);

    NoDiscount noDiscount;
    StudentDiscount studentDiscount;
    cout << "Price with no discount: " << finalPrice(1000.0, noDiscount) << '\n';
    cout << "Price after student discount: " << finalPrice(1000.0, studentDiscount) << '\n';

    CashPayment cashPayment;
    CardPayment cardPayment;
    processPayment(cashPayment, 250.0);
    processPayment(cardPayment, 250.0);

    SimplePrinter simplePrinter;
    AllInOneMachine officeMachine;
    printDocument(simplePrinter, "Math notes");
    printDocument(officeMachine, "Exam paper");
    scanDocument(officeMachine, "Signed form");

    ConsolePaymentGateway gateway;
    CheckoutService checkout(gateway);
    checkout.checkout(999.0);

    cout << '\n';
}

int main() {
    basicOopDemo();
    solidDemo();
    return 0;
}