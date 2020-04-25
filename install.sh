#!sh

rm .gdbinit
cp .gdbinit ~/.gdbinit
echo "so $(dirname $$(realpath $0))" >> ~/.gdbinit
