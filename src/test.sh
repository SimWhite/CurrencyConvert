#!/bin/bash

TEST_INPUT=(
    "1000$"
    "1,000.99$"
    "1000£"
    "35,000€"
    "299.99£"
    "1,000€"
    "441.811 USD"
    "USD 441.811"
    "3,105 JPY"
    "JPY 3,105"
    "\$898,921"
    "\$6.99"
)

COUNT=${#TEST_INPUT[@]}

for ((i=0; i<$COUNT; i++)); do
    export POPCLIP_TEXT="${TEST_INPUT[$i]}"
    printf "$POPCLIP_TEXT is: "
    python rouble.py
done
