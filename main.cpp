#include <process.h>
#include <iostream>

using namespace std;

int main() {
	_spawnl(P_WAIT, "C:\\Users\\Ángel\\source\\repos\\Proyecto\\testingprogram.exe", "C:\\Users\\Ángel\\source\\repos\\Proyecto\\test\\testingprogram.exe", NULL);
	cout << "Hello again";
	return 0;
}