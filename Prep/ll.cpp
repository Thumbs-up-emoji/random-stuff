#include <iostream>

using namespace std;

struct SNode {
	int data;
	SNode* next;

	SNode(int value) : data(value), next(nullptr) {}
};

bool hasLoop(SNode* head) {
	SNode* slow = head;
	SNode* fast = head;

	// Slow moves one step, fast moves two steps.
	while (fast != nullptr && fast->next != nullptr) {
		slow = slow->next;
		fast = fast->next->next;

		if (slow == fast) {
			return true;
		}
	}

	return false;
}

class SinglyLinkedList {
private:
	SNode* head;

public:
	SinglyLinkedList() : head(nullptr) {}

	~SinglyLinkedList() {
		clear();
	}

	void clear() {
		while (head != nullptr) {
			SNode* temp = head;
			head = head->next;
			delete temp;
		}
	}

	void append(int value) {
		SNode* newNode = new SNode(value);

		if (head == nullptr) {
			head = newNode;
			return;
		}

		SNode* current = head;
		while (current->next != nullptr) {
			current = current->next;
		}

		current->next = newNode;
	}

	void display() const {
		SNode* current = head;
		while (current != nullptr) {
			cout << current->data << ' ';
			current = current->next;
		}
		cout << '\n';
	}

	void sort() {
		// Simple value swap sort keeps the pointer logic easy to follow.
		for (SNode* first = head; first != nullptr; first = first->next) {
			for (SNode* second = first->next; second != nullptr; second = second->next) {
				if (first->data > second->data) {
					int temp = first->data;
					first->data = second->data;
					second->data = temp;
				}
			}
		}
	}

	void reverse() {
		SNode* previous = nullptr;
		SNode* current = head;

		while (current != nullptr) {
			SNode* nextNode = current->next;
			current->next = previous;
			previous = current;
			current = nextNode;
		}

		head = previous;
	}

	SNode* middle() const {
		SNode* slow = head;
		SNode* fast = head;

		while (fast != nullptr && fast->next != nullptr) {
			slow = slow->next;
			fast = fast->next->next;
		}

		return slow;
	}

	bool hasLoop() const {
		return ::hasLoop(head);
	}
};

struct DNode {
	int data;
	DNode* prev;
	DNode* next;

	DNode(int value) : data(value), prev(nullptr), next(nullptr) {}
};

bool hasLoop(DNode* head) {
	DNode* slow = head;
	DNode* fast = head;

	// Same slow/fast idea works for a DLL if we follow the next links.
	while (fast != nullptr && fast->next != nullptr) {
		slow = slow->next;
		fast = fast->next->next;

		if (slow == fast) {
			return true;
		}
	}

	return false;
}

class DoublyLinkedList {
private:
	DNode* head;

public:
	DoublyLinkedList() : head(nullptr) {}

	~DoublyLinkedList() {
		clear();
	}

	void clear() {
		while (head != nullptr) {
			DNode* temp = head;
			head = head->next;
			delete temp;
		}
	}

	void append(int value) {
		DNode* newNode = new DNode(value);

		if (head == nullptr) {
			head = newNode;
			return;
		}

		DNode* current = head;
		while (current->next != nullptr) {
			current = current->next;
		}

		current->next = newNode;
		newNode->prev = current;
	}

	void displayForward() const {
		DNode* current = head;
		while (current != nullptr) {
			cout << current->data << ' ';
			current = current->next;
		}
		cout << '\n';
	}

	void displayBackward() const {
		DNode* current = head;

		if (current == nullptr) {
			cout << '\n';
			return;
		}

		while (current->next != nullptr) {
			current = current->next;
		}

		while (current != nullptr) {
			cout << current->data << ' ';
			current = current->prev;
		}

		cout << '\n';
	}

	void sort() {
		// Simple value swap sort keeps the DLL example beginner friendly.
		for (DNode* first = head; first != nullptr; first = first->next) {
			for (DNode* second = first->next; second != nullptr; second = second->next) {
				if (first->data > second->data) {
					int temp = first->data;
					first->data = second->data;
					second->data = temp;
				}
			}
		}
	}

	void reverse() {
		DNode* current = head;
		DNode* newHead = nullptr;

		while (current != nullptr) {
			newHead = current;

			DNode* nextNode = current->next;
			current->next = current->prev;
			current->prev = nextNode;

			current = nextNode;
		}

		head = newHead;
	}

	DNode* middle() const {
		DNode* slow = head;
		DNode* fast = head;

		while (fast != nullptr && fast->next != nullptr) {
			slow = slow->next;
			fast = fast->next->next;
		}

		return slow;
	}

	bool hasLoop() const {
		return ::hasLoop(head);
	}
};

int main() {
	cout << "Singly Linked List\n";

	SinglyLinkedList ll;
	ll.append(40);
	ll.append(10);
	ll.append(30);
	ll.append(20);

	cout << "Original: ";
	ll.display();

	ll.sort();
	cout << "Sorted:   ";
	ll.display();

	ll.reverse();
	cout << "Reversed: ";
	ll.display();

	SNode* llMid = ll.middle();
	if (llMid != nullptr) {
		cout << "Middle: " << llMid->data << '\n';
	}

	cout << "Loop? " << (ll.hasLoop() ? "Yes" : "No") << '\n';

	// Manual loop demo for interview practice.
	SNode* a = new SNode(1);
	SNode* b = new SNode(2);
	SNode* c = new SNode(3);
	a->next = b;
	b->next = c;
	c->next = b;

	cout << "Manual loop demo: " << (hasLoop(a) ? "Yes" : "No") << '\n';

	c->next = nullptr;
	delete a;
	delete b;
	delete c;

	cout << "\nDoubly Linked List\n";

	DoublyLinkedList dll;
	dll.append(50);
	dll.append(15);
	dll.append(35);
	dll.append(5);

	cout << "Original: ";
	dll.displayForward();

	dll.sort();
	cout << "Sorted:   ";
	dll.displayForward();

	dll.reverse();
	cout << "Reversed: ";
	dll.displayForward();

	cout << "Backward: ";
	dll.displayBackward();

	DNode* dllMid = dll.middle();
	if (dllMid != nullptr) {
		cout << "Middle: " << dllMid->data << '\n';
	}

	cout << "Loop? " << (dll.hasLoop() ? "Yes" : "No") << '\n';

	// Manual DLL loop demo.
	DNode* x = new DNode(7);
	DNode* y = new DNode(8);
	DNode* z = new DNode(9);
	x->next = y;
	y->prev = x;
	y->next = z;
	z->prev = y;
	z->next = y;

	cout << "Manual DLL loop demo: " << (hasLoop(x) ? "Yes" : "No") << '\n';

	z->next = nullptr;
	delete x;
	delete y;
	delete z;

	return 0;
}
