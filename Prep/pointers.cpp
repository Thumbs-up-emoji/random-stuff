#include <iostream>
#include <memory>
#include <string>

using namespace std;

// C++ revision notes: pointers.
// This file is a small runnable walkthrough of the core ideas.

struct Student {
	string name;
	int age;

	void print() const {
		cout << "Student(name = " << name << ", age = " << age << ")\n";
	}
};

void printSection(const char* title) {
	cout << "\n=== " << title << " ===\n";
}

void basicPointerDemo() {
	printSection("Basic pointer");

	int marks = 95;
	int* pointer = &marks;

	cout << "marks value: " << marks << '\n';
	cout << "address of marks: " << &marks << '\n';
	cout << "pointer stores: " << pointer << '\n';
	cout << "dereferenced pointer: " << *pointer << '\n';

	*pointer = 100;
	cout << "after *pointer = 100, marks: " << marks << '\n';
}
void nullPointerDemo() {
	printSection("Null pointer");

	int* pointer = nullptr;

	if (pointer == nullptr) {
		cout << "pointer is null, so do not dereference it.\n";
	}
}

void pointerToPointerDemo() {
	printSection("Pointer to pointer");

	int value = 7;
	int* pointer = &value;
	int** pointerToPointer = &pointer;

	cout << "value: " << value << '\n';
	cout << "pointer: " << pointer << '\n';
	cout << "pointerToPointer: " << pointerToPointer << '\n';
	cout << "**pointerToPointer: " << **pointerToPointer << '\n';
}

void arrayAndPointerDemo() {
	printSection("Array and pointer arithmetic");

	int numbers[] = {10, 20, 30, 40};
	int* pointer = numbers;

	cout << "numbers[0] via pointer: " << *pointer << '\n';
	cout << "numbers[2] via pointer arithmetic: " << *(pointer + 2) << '\n';

	for (int index = 0; index < 4; ++index) {
		cout << "element " << index << " at " << (pointer + index)
			 << " = " << *(pointer + index) << '\n';
	}
}

void constPointerDemo() {	// With extra pointer arithmetic examples.
	printSection("Const with pointers");

	int first = 5;
	int second = 10;

	const int* pointerToConst = &first;
    // The pointer can move to another int.
    // The int it points to cannot be changed through this name.
    cout << "pointerToConst points to: " << *pointerToConst << '\n';
    pointerToConst = &second;
    cout << "pointerToConst now points to: " << *pointerToConst << '\n';

    int* const constPointer = &first;
    // The pointer itself is fixed.
    // The int it points to can still be changed.
    *constPointer = 15;
    cout << "after *constPointer = 15, first: " << first << '\n';

    const int* const constPointerToConst = &second;
    // Fixed pointer, and read-only view of the int.
    cout << "constPointerToConst: " << *constPointerToConst << '\n';

    int values[] = {5, 10, 15, 20};

    int* standardPointer = values;
    // Normal pointer: it can move, and it can modify the array values.
    cout << "standardPointer starts at: " << *standardPointer << '\n';
    cout << "standardPointer + 2: " << *(standardPointer + 2) << '\n';
    ++standardPointer;
    cout << "after ++standardPointer: " << *standardPointer << '\n';

    const int* pointerToConstArithmetic = values;
    // Can move through the array, but cannot modify values through this pointer.
    cout << "pointerToConstArithmetic starts at: " << *pointerToConstArithmetic << '\n';
    cout << "pointerToConstArithmetic + 1: " << *(pointerToConstArithmetic + 1) << '\n';
    pointerToConstArithmetic += 2;
    cout << "after pointerToConstArithmetic += 2: " << *pointerToConstArithmetic << '\n';

    int* const fixedPointer = values;
    // Fixed address, but still writable.
    *fixedPointer = 50;
    cout << "after *fixedPointer = 50, values[0]: " << values[0] << '\n';
    cout << "fixedPointer + 3: " << *(fixedPointer + 3) << '\n';

    const int* const fixedPointerToConst = values;
    // Fixed address and read-only view.
    cout << "fixedPointerToConst: " << *fixedPointerToConst << '\n';
    cout << "fixedPointerToConst + 3: " << *(fixedPointerToConst + 3) << '\n';
}

void objectPointerDemo() {
	printSection("Pointer to object");

	Student student;
	student.age = 20;
	student.name = to_string(student.age);
	Student* pointer = &student;

	student.print();
	pointer->print();

	pointer->age = 21;
	cout << "after pointer->age = 21:\n";
	student.print();
}

void smartPointerDemo() {
	printSection("Smart pointer for ownership");

	unique_ptr<int> owned = make_unique<int>(42);
	cout << "unique_ptr value: " << *owned << '\n';
	cout << "Use smart pointers when the pointer owns memory.\n";
}

int main() {
	cout << "C++ pointer revision\n";
	cout << "Key operators: & gets an address, * dereferences, -> accesses a member through a pointer.\n";

	basicPointerDemo();
	nullPointerDemo();
	pointerToPointerDemo();
	arrayAndPointerDemo();
	constPointerDemo();
	objectPointerDemo();
	// smartPointerDemo();

	return 0;
}
