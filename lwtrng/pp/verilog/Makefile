python_path = ..
verilog_files = DuplexingPP.v

all: $(verilog_files)

DuplexingPP.v: $(python_path)/duplexing.py

%.v:
	python $< generate -t v > $@

clean:
	rm -rf *.v
