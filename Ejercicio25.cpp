#include <iostream>

const int TAM = 500001;

struct tLista {
	int n = 0;
	int p = 0;
	int a[TAM];
};

void resuelveCaso() {
	tLista caso;
	std::cin >> caso.n >> caso.p;
	for (int i = 0; i < caso.n; ++i)
		std::cin >> caso.a[i];
	if (caso.p == caso.n - 1) {
		std::cout << "SI\n";
	}
	else {
		int valorMax = caso.a[0];
		for (int i = 0; i <= caso.p; ++i) {
			if (valorMax <= caso.a[i])
				valorMax = caso.a[i];
		}
		int valorMin = caso.a[caso.p + 1];
		for (int i = caso.p + 1; i < caso.n; ++i) {
			if (valorMin >= caso.a[i])
				valorMin = caso.a[i];
		}
		if (valorMax < valorMin) 
			std::cout<< "SI\n";
		else
			std::cout<< "NO\n";
	}
}

int main() {
	int numCasos;
	std::cin >> numCasos;
	for (int i = 0; i < numCasos; ++i)
		resuelveCaso();
	return 0;
}