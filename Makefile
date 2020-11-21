FILE=password_cracker
BIN_PATH=bin

compile:
	gcc $(FILE).c  -l crypto -o $(FILE).o
	mkdir -p $(BIN_PATH)
	mv $(FILE).o $(BIN_PATH)

clean:
	rm -rf $(BIN_PATH)

