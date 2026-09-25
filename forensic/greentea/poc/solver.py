import struct, subprocess

#read payload file .rtp
payloads = []
with open('teh_hijau_challenge.rtp', 'rb') as f:
    f.readline() # Header text
    f.read(16)   # Header binary
    while True:
        rec = f.read(8)
        if len(rec) < 8: break
        length, plen, offset = struct.unpack('>HHI', rec)
        data = f.read(plen)
        if len(data) >= 12:
            payloads.append(data[12:]) # Buang 12-byte header RTP

# wrap ke format LOAS (Low-Overhead Audio Stream)
with open('stream.loas', 'wb') as f:
    for p in payloads:
        hdr = (0x2B7 << 13) | (len(p) & 0x1FFF)
        f.write(struct.pack('>I', hdr)[1:] + p)

# decode ke file WAV
subprocess.run(['ffmpeg', '-y', '-i', 'stream.loas', 'lagu_hasil_ekstrak.wav'])
