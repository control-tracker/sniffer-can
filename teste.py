import random

def generate_random_timestamp():
    return random.randint(10000000, 99999999)

def parse_line(line):
    if line.startswith("Extended ID:"):
        # Formato 1: Extended ID: 0x1CFEEFFF  DLC: 8  Data: 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF
        parts = line.split()
        if len(parts) < 7:
            raise ValueError(f"Formato inválido: {line}")
        extended_id = parts[2]
        data_bytes = parts[6:]
    else:
        # Formato 2: Priority: 2, PGN: 65325, from 0x08FF2D3F, DLC 8, Data: 0x04 0xDE 0x00 0x00 0x00 0x00 0xFF 0xFF
        parts = line.split(',')
        if len(parts) < 5:
            raise ValueError(f"Formato inválido: {line}")
        from_part = parts[2].strip().split()
        if len(from_part) < 2:
            raise ValueError(f"Formato inválido: {line}")
        extended_id = from_part[1]
        data_part = line.split("Data:")[1].strip()
        data_bytes = data_part.split()

    # Remover o '0x' dos valores hexadecimais e converter para maiúsculas
    extended_id = extended_id[2:].upper()
    data_bytes = [byte[2:].upper() for byte in data_bytes]

    # Gerar um timestamp aleatório
    timestamp = generate_random_timestamp()

    # Criar a nova linha no formato desejado
    new_line = f"{int(extended_id, 16)},{extended_id},true,Rx,0,8," + ",".join(data_bytes) + ","
    return new_line

def convert_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                new_line = parse_line(line)
                outfile.write(new_line + '\n')
            except ValueError as e:
                print(f"Erro ao processar a linha: {e}")

# Especifique os nomes dos arquivos de entrada e saída
input_file = 'sniffer vw constellation.txt'
output_file = 'sniffer vw constellation a.txt'

# Execute a conversão
convert_file(input_file, output_file)
