# Packer
API Module to pack games and other data in an efficient and quickshare way.

> [!NOTE]
> Packed Data can only be unpacked by the integrated API !Do NOT unpack it manually!

## How it works

The Upload in many alternatives is based either on FTP or similar Protocols which is in turn not bad but
the biggest problem is that for example Games are TOO big which makes this process take ages.
So my idea was to speed this process up by breaking down the file packages and transfering them multithreaded this way.

The notice on top is a side product of that as no unpacker exists to do this outside from this projects internal one.

As all files are basicly in one big directory and not broken down We need some sort of indexing file to tell the system where
these files need to go.
