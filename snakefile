import os

def remove_extension(string):
    return string[:string.rfind('.')]

def remove_path(string):
    return string[string.rfind('/')+1:]

configfile: "config.yaml"

draft=remove_path(remove_extension(config["draft"]))
ref=remove_path(remove_extension(config["ref"]))

rule all:
    input:
        expand("{draft}_to_{ref}.NG{ng}.chained.subsumed.coloured.png", draft=draft, ref=ref, ng=config["ng"])

rule map_assembly_to_reference:
    input: 
        ref = expand("{ref}.renamed.fa", ref=remove_extension(config["ref"])),
        draft = config["draft"]
    output: 
        expand("{draft}_to_{ref}.bam", draft=draft, ref=ref)
    threads:
        config["threads"]
    shell: 
        "minimap2 -t{threads} -ax asm5 {input.ref} {input.draft} | samtools view -bS - > {output}"

rule bam_to_bed:
    input: 
        expand("{draft}_to_{ref}.bam", draft=draft, ref=ref)
    output: 
        expand("{draft}_to_{ref}.bed", draft=draft, ref=ref)
    shell: 
        "bedtools bamtobed -i {input} > {output}"

rule extract_NGXX_entries_from_bed:
    input:
        bed = expand("{draft}_to_{ref}.bed", draft=draft, ref=ref),
        ref = expand("{ref}.renamed.fa", ref=remove_extension(config["ref"])),
        draft = config["draft"]
    output:
        expand("{draft}_to_{ref}.NG{ng}.bed", draft=draft, ref=ref, ng=config["ng"])
    params:
        ng = config["ng"]
    shell:
        "python print_bed_entries_with_NGXX.py --bed {input.bed} --ref {input.ref} --draft {input.draft} --ng {params.ng} | bedtools sort -i - > {output}"

rule chain_bed_entries:
    input: 
        expand("{draft}_to_{ref}.NG{ng}.bed", draft=draft, ref=ref, ng=config["ng"])
    output:
        expand("{draft}_to_{ref}.NG{ng}.chained.bed", draft=draft, ref=ref, ng=config["ng"])
    params:
        dist = config["dist"]
    shell:
        "python chain_bed_entries.py --bed {input} --dist {params.dist} | bedtools sort -i - > {output}"

rule remove_subsumed_entries:
    input: 
        expand("{draft}_to_{ref}.NG{ng}.chained.bed", draft=draft, ref=ref, ng=config["ng"])
    output:
        expand("{draft}_to_{ref}.NG{ng}.chained.subsumed.bed", draft=draft, ref=ref, ng=config["ng"])
    shell:
        "python remove_subsumed_bed_entries.py --bed {input} | bedtools sort -i - > {output}"

rule colour_bed_entries:
    input: 
        expand("{draft}_to_{ref}.NG{ng}.chained.subsumed.bed", draft=draft, ref=ref, ng=config["ng"])
    output:
        expand("{draft}_to_{ref}.NG{ng}.chained.subsumed.coloured.bed", draft=draft, ref=ref, ng=config["ng"])
    shell:
        "python colour_bed_entries.py --bed {input} > {output}"

rule plot_ideogram:
    input: 
        expand("{draft}_to_{ref}.NG{ng}.chained.subsumed.coloured.bed", draft=draft, ref=ref, ng=config["ng"])
    output: 
        expand("{draft}_to_{ref}.NG{ng}.chained.subsumed.coloured.png", draft=draft, ref=ref, ng=config["ng"])
    shell:
        "Rscript plot_ideogram.r {input} {output}"

rule rename_ref:
    input: 
        config["ref"]
    output: 
        expand("{ref}.renamed.fa", ref=ref)
    shell:
        "python rename_ref.py --ref {input} > {output}"
