#!/bin/bash

function build_mdconverter {
	git clone git@github.com:Menta-Epitech-Academy/mdConverter.git
	cd mdConverter
	docker build . --rm --tag mdconverter
	cd -
}

function gen_subject {
	docker run --rm -v $PWD:/ARTIFACTS -it mdconverter -y Linux.yaml -d Linux.md
}

build_mdconverter && gen_subject
