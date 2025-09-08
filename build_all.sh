#!/bin/bash

cd subject && ./build.sh && cd - && cd v86lab && ./build.sh && cp ../subject/Linux_academy.pdf dist/subject.pdf

