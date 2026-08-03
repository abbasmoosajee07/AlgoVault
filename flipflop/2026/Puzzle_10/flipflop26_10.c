/* FlipFlop 2026: BitFlop Internship - Puzzle 10
Solution Started: August 3, 2026
Puzzle Link: https://flipflop.slome.org/2026/10
Solution by: Abbas Moosajee
Brief: [The Banena™ Programming Language]

C translation of the original Rust solution. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>

/* ---------------------------------------------------------------------- */
/* Instruction representation                                             */
/* ---------------------------------------------------------------------- */

typedef enum {
    OP_LOAD,
    OP_COPY,
    OP_ADD,
    OP_SUB,
    OP_MUL,
    OP_MOD,
    OP_INC,
    OP_DEC,
    OP_JMP,
    OP_JZ,
    OP_JNZ,
} OpCode;

typedef struct {
    OpCode op;
    union {
        struct { uint16_t val; size_t dest_reg; } load;
        struct { size_t src_reg, dest_reg; } copy;
        struct { size_t src_reg1, src_reg2, dest_reg; } arith; /* add/sub/mul/mod */
        struct { size_t reg; } single;                          /* inc/dec */
        struct { size_t label; } jmp;                            /* jmp */
        struct { size_t reg, label; } cjmp;                      /* jz/jnz */
    } u;
} Instruction;

static void instr_print(const Instruction *ins) {
    switch (ins->op) {
        case OP_LOAD: printf("mov %u -> r%zu\n", ins->u.load.val, ins->u.load.dest_reg); break;
        case OP_COPY: printf("mov r%zu -> r%zu\n", ins->u.copy.src_reg, ins->u.copy.dest_reg); break;
        case OP_ADD:  printf("add r%zu + r%zu -> r%zu\n", ins->u.arith.src_reg1, ins->u.arith.src_reg2, ins->u.arith.dest_reg); break;
        case OP_SUB:  printf("sub r%zu - r%zu -> r%zu\n", ins->u.arith.src_reg1, ins->u.arith.src_reg2, ins->u.arith.dest_reg); break;
        case OP_MUL:  printf("mul r%zu * r%zu -> r%zu\n", ins->u.arith.src_reg1, ins->u.arith.src_reg2, ins->u.arith.dest_reg); break;
        case OP_MOD:  printf("mod r%zu %% r%zu -> r%zu\n", ins->u.arith.src_reg1, ins->u.arith.src_reg2, ins->u.arith.dest_reg); break;
        case OP_INC:  printf("inc r%zu\n", ins->u.single.reg); break;
        case OP_DEC:  printf("dec r%zu\n", ins->u.single.reg); break;
        case OP_JMP:  printf("jmp %zu\n", ins->u.jmp.label); break;
        case OP_JZ:   printf("jz  r%zu %zu\n", ins->u.cjmp.reg, ins->u.cjmp.label); break;
        case OP_JNZ:  printf("jnz r%zu %zu\n", ins->u.cjmp.reg, ins->u.cjmp.label); break;
    }
}

/* ---------------------------------------------------------------------- */
/* Dynamic program buffer                                                 */
/* ---------------------------------------------------------------------- */

typedef struct {
    Instruction *data;
    size_t len;
    size_t cap;
} Program;

static void program_init(Program *p) {
    p->data = NULL;
    p->len = 0;
    p->cap = 0;
}

static void program_push(Program *p, Instruction ins) {
    if (p->len == p->cap) {
        p->cap = p->cap == 0 ? 16 : p->cap * 2;
        p->data = realloc(p->data, p->cap * sizeof(Instruction));
        if (!p->data) {
            fprintf(stderr, "out of memory\n");
            exit(1);
        }
    }
    p->data[p->len++] = ins;
}

/* ---------------------------------------------------------------------- */
/* Simple label map: label (size_t) -> program index (size_t)             */
/* ---------------------------------------------------------------------- */

typedef struct {
    size_t key;
    size_t value;
} LabelEntry;

typedef struct {
    LabelEntry *data;
    size_t len;
    size_t cap;
} LabelMap;

static void labelmap_init(LabelMap *m) {
    m->data = NULL;
    m->len = 0;
    m->cap = 0;
}

static void labelmap_insert(LabelMap *m, size_t key, size_t value) {
    if (m->len == m->cap) {
        m->cap = m->cap == 0 ? 16 : m->cap * 2;
        m->data = realloc(m->data, m->cap * sizeof(LabelEntry));
        if (!m->data) {
            fprintf(stderr, "out of memory\n");
            exit(1);
        }
    }
    m->data[m->len].key = key;
    m->data[m->len].value = value;
    m->len++;
}

static size_t labelmap_get(const LabelMap *m, size_t key) {
    for (size_t i = 0; i < m->len; i++) {
        if (m->data[i].key == key) {
            return m->data[i].value;
        }
    }
    fprintf(stderr, "label %zu not found\n", key);
    exit(1);
}

/* ---------------------------------------------------------------------- */
/* Parsing                                                                 */
/* ---------------------------------------------------------------------- */

/* Mirrors the Rust `nas` closure: counts consecutive "na" 2-byte chunks
 * starting at *pos, consuming (advancing pos past) one extra terminating
 * chunk if the iterator is not exhausted -- matching take_while().count()
 * semantics on a shared, resumable iterator. */
static size_t nas(const char *line, int num_chunks, int *pos) {
    size_t count = 0;
    while (*pos < num_chunks) {
        const char *chunk = line + (*pos) * 2;
        (*pos)++;
        if (strncmp(chunk, "na", 2) == 0) {
            count++;
        } else {
            break;
        }
    }
    return count;
}

/* Portable replacement for POSIX getline(): reads one line (of any length)
 * into a growable buffer, reallocating as needed. Returns the number of
 * bytes read (not including the terminator) or -1 at EOF with nothing read. */
static long read_line(FILE *f, char **buf, size_t *cap) {
    if (*cap == 0) {
        *cap = 256;
        *buf = malloc(*cap);
        if (!*buf) {
            fprintf(stderr, "out of memory\n");
            exit(1);
        }
    }

    size_t len = 0;
    for (;;) {
        if (len + 1 >= *cap) {
            *cap *= 2;
            char *grown = realloc(*buf, *cap);
            if (!grown) {
                fprintf(stderr, "out of memory\n");
                exit(1);
            }
            *buf = grown;
        }

        if (!fgets(*buf + len, (int)(*cap - len), f)) {
            break; /* EOF or error */
        }

        len += strlen(*buf + len);

        if (len > 0 && (*buf)[len - 1] == '\n') {
            break; /* full line read */
        }
        if (feof(f)) {
            break; /* last line, no trailing newline */
        }
        /* otherwise the buffer was too small for the whole line; loop and grow */
    }

    if (len == 0 && feof(f)) {
        return -1;
    }
    return (long)len;
}

static Program parse_program(const char *file_path, LabelMap *labels) {
    Program program;
    program_init(&program);
    labelmap_init(labels);

    FILE *f = fopen(file_path, "r");
    if (!f) {
        fprintf(stderr, "failed to open %s: %s\n", file_path, strerror(errno));
        exit(1);
    }

    char *line = NULL;
    size_t line_cap = 0;
    long nread;

    while ((nread = read_line(f, &line, &line_cap)) != -1) {
        /* Trim trailing newline / carriage return, matching Rust's line() */
        while (nread > 0 && (line[nread - 1] == '\n' || line[nread - 1] == '\r')) {
            nread--;
        }
        line[nread] = '\0';

        int num_chunks = (int)(nread / 2); /* chunks_exact(2) drops any trailing odd byte */
        if (num_chunks == 0) {
            continue;
        }

        int pos = 0;
        const char *first_chunk = line + pos * 2;
        pos = 1;

        if (strncmp(first_chunk, "ba", 2) != 0) {
            /* Label line: label value is the number of remaining chunks
             * after consuming the first one. */
            size_t label = (size_t)(num_chunks - 1);
            labelmap_insert(labels, label, program.len);
            continue;
        }

        size_t instr = nas(line, num_chunks, &pos);
        Instruction ins;
        switch (instr) {
            case 0:
                ins.op = OP_LOAD;
                ins.u.load.val = (uint16_t)nas(line, num_chunks, &pos);
                ins.u.load.dest_reg = nas(line, num_chunks, &pos);
                break;
            case 1:
                ins.op = OP_COPY;
                ins.u.copy.src_reg = nas(line, num_chunks, &pos);
                ins.u.copy.dest_reg = nas(line, num_chunks, &pos);
                break;
            case 2:
                ins.op = OP_ADD;
                ins.u.arith.src_reg1 = nas(line, num_chunks, &pos);
                ins.u.arith.src_reg2 = nas(line, num_chunks, &pos);
                ins.u.arith.dest_reg = nas(line, num_chunks, &pos);
                break;
            case 3:
                ins.op = OP_SUB;
                ins.u.arith.src_reg1 = nas(line, num_chunks, &pos);
                ins.u.arith.src_reg2 = nas(line, num_chunks, &pos);
                ins.u.arith.dest_reg = nas(line, num_chunks, &pos);
                break;
            case 4:
                ins.op = OP_MUL;
                ins.u.arith.src_reg1 = nas(line, num_chunks, &pos);
                ins.u.arith.src_reg2 = nas(line, num_chunks, &pos);
                ins.u.arith.dest_reg = nas(line, num_chunks, &pos);
                break;
            case 5:
                ins.op = OP_MOD;
                ins.u.arith.src_reg1 = nas(line, num_chunks, &pos);
                ins.u.arith.src_reg2 = nas(line, num_chunks, &pos);
                ins.u.arith.dest_reg = nas(line, num_chunks, &pos);
                break;
            case 6:
                ins.op = OP_INC;
                ins.u.single.reg = nas(line, num_chunks, &pos);
                break;
            case 7:
                ins.op = OP_DEC;
                ins.u.single.reg = nas(line, num_chunks, &pos);
                break;
            case 8:
                ins.op = OP_JMP;
                ins.u.jmp.label = nas(line, num_chunks, &pos);
                break;
            case 9:
                ins.op = OP_JZ;
                ins.u.cjmp.reg = nas(line, num_chunks, &pos);
                ins.u.cjmp.label = nas(line, num_chunks, &pos);
                break;
            case 10:
                ins.op = OP_JNZ;
                ins.u.cjmp.reg = nas(line, num_chunks, &pos);
                ins.u.cjmp.label = nas(line, num_chunks, &pos);
                break;
            default:
                fprintf(stderr, "unimplemented instr %zu\n", instr);
                exit(1);
        }
        program_push(&program, ins);
    }

    free(line);
    fclose(f);
    return program;
}

/* ---------------------------------------------------------------------- */
/* Execution                                                               */
/* ---------------------------------------------------------------------- */

/* Returns 1 (Some) with *result set, or 0 (None) if the instruction budget
 * is exceeded, matching the Rust Option<u16> return value. */
static int exec_program(const Program *program, const LabelMap *labels,
                         uint16_t init_r0, uint16_t init_r1, uint16_t *result) {
    size_t pc = 0;
    uint16_t regs[16] = {0};
    regs[0] = init_r0;
    regs[1] = init_r1;
    long instrs = 0;

    while (pc < program->len) {
        instrs++;
        if (instrs > 5000000) {
            return 0;
        }

        const Instruction *ins = &program->data[pc];
        switch (ins->op) {
            case OP_LOAD:
                regs[ins->u.load.dest_reg] = ins->u.load.val;
                break;
            case OP_COPY:
                regs[ins->u.copy.dest_reg] = regs[ins->u.copy.src_reg];
                break;
            case OP_ADD:
                regs[ins->u.arith.dest_reg] =
                    (uint16_t)(regs[ins->u.arith.src_reg1] + regs[ins->u.arith.src_reg2]);
                break;
            case OP_SUB:
                regs[ins->u.arith.dest_reg] =
                    (uint16_t)(regs[ins->u.arith.src_reg1] - regs[ins->u.arith.src_reg2]);
                break;
            case OP_MUL:
                regs[ins->u.arith.dest_reg] =
                    (uint16_t)(regs[ins->u.arith.src_reg1] * regs[ins->u.arith.src_reg2]);
                break;
            case OP_MOD: {
                uint16_t divisor = regs[ins->u.arith.src_reg2];
                regs[ins->u.arith.dest_reg] =
                    divisor != 0 ? (uint16_t)(regs[ins->u.arith.src_reg1] % divisor) : 0;
                break;
            }
            case OP_INC:
                regs[ins->u.single.reg] = (uint16_t)(regs[ins->u.single.reg] + 1);
                break;
            case OP_DEC:
                regs[ins->u.single.reg] = (uint16_t)(regs[ins->u.single.reg] - 1);
                break;
            case OP_JMP:
                pc = labelmap_get(labels, ins->u.jmp.label);
                continue;
            case OP_JZ:
                if (regs[ins->u.cjmp.reg] == 0) {
                    pc = labelmap_get(labels, ins->u.cjmp.label);
                    continue;
                }
                break;
            case OP_JNZ:
                if (regs[ins->u.cjmp.reg] != 0) {
                    pc = labelmap_get(labels, ins->u.cjmp.label);
                    continue;
                }
                break;
        }
        pc++;
    }

    *result = regs[0];
    return 1;
}

static uint16_t solve_part1(const Program *program, const LabelMap *labels) {
    uint16_t result;
    if (!exec_program(program, labels, 0, 0, &result)) {
        fprintf(stderr, "part1: program did not terminate\n");
        exit(1);
    }
    return result;
}

static size_t solve_part2(const Program *program, const LabelMap *labels) {
    size_t none_count = 0;
    for (uint16_t r0 = 0; r0 < 100; r0++) {
        uint16_t result;
        if (!exec_program(program, labels, r0, 0, &result)) {
            none_count++;
        }
    }
    return none_count;
}

static size_t solve_part3(const Program *program, const LabelMap *labels) {
    size_t total = 0;
    for (uint16_t r1 = 0; r1 < 16; r1++) {
        size_t none_count = 0;
        for (uint16_t r0 = 0; r0 < 16; r0++) {
            uint16_t result;
            if (!exec_program(program, labels, r0, r1, &result)) {
                none_count++;
            }
        }
        total += none_count * (65536 / 16);
    }
    return total;
}

static const char *get_file_path(int argc, char **argv) {
    if (argc > 1) {
        return argv[1];
    }
    return "puzzle_10_input.txt";
}

int main(int argc, char **argv) {
    const char *file_path = get_file_path(argc, argv);

    LabelMap labels;
    Program program = parse_program(file_path, &labels);

    uint16_t part1 = solve_part1(&program, &labels);
    size_t part2 = solve_part2(&program, &labels);
    size_t part3 = solve_part3(&program, &labels);

    printf("FlipFlop 2026, Puzzle 10\n");
    printf("Part 1: %u\n", part1);
    printf("Part 2: %zu\n", part2);
    printf("Part 3: %zu\n", part3);

    free(program.data);
    free(labels.data);
    return 0;
}