#!/bin/bash

usage() {
    echo "Usage: $0 -f <csv_file> -a <api_key> -s <seed> -m <model_name> -o <out_dir> [-i <start_row>] [-j <end_row>]"
    exit 1
}

while getopts ":f:i:j:a:o:s:m:" opt; do
    case $opt in
        f) csv_file="$OPTARG" ;;
        i) start_row="$OPTARG" ;;
        j) end_row="$OPTARG" ;;
        a) api_key="$OPTARG" ;;
        o) out_dir="$OPTARG" ;;
        s) seed="$OPTARG" ;;
        m) model_name="$OPTARG" ;;
        *) usage ;;
    esac
done

if [[ -z "$csv_file" ]]; then
    usage
fi

if ! [[ -f "$csv_file" ]]; then
    echo "Error: File '$csv_file' not found."
    exit 1
fi

header_read=false
row_num=0
while IFS=',' read -r line; do
    ((row_num++))
    if [[ "$header_read" == false ]]; then
        IFS=',' read -r -a keys <<< "$line"
        header_read=true
        continue
    fi
    if [[ -n "$start_row" && "$row_num" -lt "$start_row" ]]; then
        continue
    fi
    if [[ -n "$end_row" && "$row_num" -gt "$end_row" ]]; then
        break
    fi
    IFS=',' read -r -a values <<< "$line"
    args=()
    for i in "${!keys[@]}"; do
        args+=("--${keys[i]}" "${values[i]}")
    done

    echo "--out_dir $out_dir --api_key $api_key --model_name $model_name --seed $seed ${args[@]}"

    python3 soc_distrust_panel.py \
        "$out_dir" \
        "$api_key" \
        --model_name "$model_name" \
        --seed $seed \
        "${args[@]}"

done < "$csv_file"
