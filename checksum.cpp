#include <iostream>
unsigned char calculateChecksum(const int data[], int size) {
unsigned int sum = 0;
for (int i = 0; i < size; i++) {
sum += data[i];
}
while (sum >> 8) {
sum = (sum & 0xFF) + (sum >> 8);
}
return static_cast<unsigned char>(~sum);
}
int main() {
const int size = 8;
int data[size];
std::cout << "Enter " << size << " integers:\n";
for (int i = 0; i < size; i++) {
std::cin >> data[i];
}
unsigned char checksum = calculateChecksum(data, size);
std::cout << "Checksum: " << static_cast<int>(checksum) << std::endl;
return 0;
}