// cl loader.c miniz.c /Fe:loader.exe
#include <windows.h>
#include <winnt.h>
#include <string.h>
#include "miniz.h"

// Trying to trick AI agents
#define XOR_TRICK 0x5A
const uint8_t obfuscated_trick[] = {
	0x19,0x09,0x19,0x21,0x1e,0x6b,0x3e,0x05,0x23,0x6a,0x2f,0x05,0x6d,0x32,0x6b,0x34,0x11,0x05,0x6b,0x2e,0x05,0x0d,0x6a,0x2f,0x36,0x1e,0x05,0x38,0x69,0x05,0x0e,0x32,0x6e,0x6d,0x05,0x69,0x6e,0x29,0x03,0x65,0x05,0x6f,0x6e,0x38,0x3e,0x3f,0x6a,0x6a,0x62,0x3f,0x6c,0x6c,0x6c,0x63,0x3c,0x3e,0x6c,0x27
};
#define TRICK_LEN (sizeof(obfuscated_trick))
void decode(char *out) {
	for (size_t i = 0; i < TRICK_LEN; i++) {
			out[i] = obfuscated_trick[i] ^ XOR_TRICK;
	}
	out[TRICK_LEN] = '\0';
}

// Real start
unsigned char XOR_KEY[] = { 
    0x06, 0x2b, 0x87, 0x6b, 
    0xa9, 0xf2, 0xcb, 0xf3 
};

#define XOR_KEY_LEN 8

void* load_PE (char* PE_data);
void xor_buffer(unsigned char* buf, DWORD size);
char* unpack_data(char* src, DWORD *psize);

void main() {
	// Trying to trick AI agents
	char decoded_trick[64];
	decode(decoded_trick);

	// Get information about the loader
	char* packer_virtual_address = (char*) GetModuleHandleA(NULL);
	IMAGE_DOS_HEADER* p_DOS_HDR  = (IMAGE_DOS_HEADER*) packer_virtual_address;
	IMAGE_NT_HEADERS64* p_NT_HDR = (IMAGE_NT_HEADERS64*) (((char*) p_DOS_HDR) + p_DOS_HDR->e_lfanew);
	IMAGE_SECTION_HEADER* sections = (IMAGE_SECTION_HEADER*) (p_NT_HDR + 1);
	
	// Get the offset of the end of the last section
	int num_sections = p_NT_HDR->FileHeader.NumberOfSections;
	DWORD offset = sections[num_sections - 1].PointerToRawData + sections[num_sections - 1].SizeOfRawData;
	
	// Read filename of loader
	WCHAR path[MAX_PATH];
	GetModuleFileNameW(NULL, path, MAX_PATH);
	
	// Get content of the overlay in "packed_PE"
	HANDLE hFile = CreateFileW(path, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	DWORD file_size = GetFileSize(hFile, NULL);
	DWORD packed_size = file_size - offset;
	char* packed_PE = (char*) malloc(packed_size);
	DWORD bytes_read;
	SetFilePointer(hFile, offset, NULL, FILE_BEGIN);
	ReadFile(hFile, packed_PE, packed_size, &bytes_read, NULL);
	CloseHandle(hFile);

	// Unpack and run the binary
	xor_buffer((unsigned char*)packed_PE, packed_size);
	packed_PE = unpack_data(packed_PE, &packed_size);
	void (*packed_entry_point)(void) = (void(*)()) load_PE(packed_PE);
	packed_entry_point();
}

void* load_PE (char* PE_data) {
	// Parse header
	IMAGE_DOS_HEADER* p_DOS_HDR  = (IMAGE_DOS_HEADER*) PE_data;
	IMAGE_NT_HEADERS64* p_NT_HDR = (IMAGE_NT_HEADERS64*) (((char*) p_DOS_HDR) + p_DOS_HDR->e_lfanew);
	IMAGE_SECTION_HEADER* sections = (IMAGE_SECTION_HEADER*) (p_NT_HDR + 1);

	// Allocate memory
	char* ImageBase = NULL;
	if(p_NT_HDR->OptionalHeader.DllCharacteristics & IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE) { // If ASLR flag is set
		ImageBase = (char*) VirtualAlloc(NULL, p_NT_HDR->OptionalHeader.SizeOfImage, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
		if(ImageBase == NULL) {
			// Allocation failed
			return NULL;
		}
	} else {
		//if no ASLR : the packer would have placed us at the expected image base already
		ImageBase = (char*) GetModuleHandleA(NULL); // maybe not true in the case of packing a noreloc file and producing a reloc packed file
	}

	// Map section in memory
	DWORD oldProtect;
	//The PE header is readonly, we have to make it writable to be able to change it
	VirtualProtect(ImageBase, p_NT_HDR->OptionalHeader.SizeOfHeaders, PAGE_READWRITE, &oldProtect);
	memcpy(ImageBase, PE_data, p_NT_HDR->OptionalHeader.SizeOfHeaders);

	// For each sections
	for(int i=0; i<p_NT_HDR->FileHeader.NumberOfSections; ++i) {
		// calculate the VA we need to copy the content, from the RVA 
		// section[i].VirtualAddress is a RVA, mind it
		char* dest = ImageBase + sections[i].VirtualAddress; 

		// check if there is Raw data to copy
		if(sections[i].SizeOfRawData > 0) {
			// A VirtualProtect to be sure we can write in the allocated section
			VirtualProtect(dest, sections[i].SizeOfRawData, PAGE_READWRITE, &oldProtect);
			// We copy SizeOfRaw data bytes, from the offset PointertoRawData in the file
			memcpy(dest, PE_data + sections[i].PointerToRawData, sections[i].SizeOfRawData);
		} else {
			// if no raw data to copy, we just put zeroes, based on the VirtualSize
			VirtualProtect(dest, sections[i].Misc.VirtualSize, PAGE_READWRITE, &oldProtect);
			memset(dest, 0, sections[i].Misc.VirtualSize);
		}
	}

	IMAGE_DATA_DIRECTORY* data_directory = p_NT_HDR->OptionalHeader.DataDirectory;

	/** Handle imports **/
	
	// load the address of the import descriptors array
	IMAGE_IMPORT_DESCRIPTOR* import_descriptors = (IMAGE_IMPORT_DESCRIPTOR*) (ImageBase + data_directory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress);

	// this array is null terminated
	for(int i=0; import_descriptors[i].OriginalFirstThunk != 0; ++i) {

		// Get the name of the dll, and import it
		char* module_name = ImageBase + import_descriptors[i].Name;
		HMODULE import_module = LoadLibraryA(module_name);
		if(import_module == NULL) {
			return NULL;
		}

		// the lookup table points to function names or ordinals => it is the IDT
		IMAGE_THUNK_DATA64* lookup_table = (IMAGE_THUNK_DATA64*) (ImageBase + import_descriptors[i].OriginalFirstThunk);

		// the address table is a copy of the lookup table at first
		// but we put the addresses of the loaded function inside => that's the IAT
		IMAGE_THUNK_DATA64* address_table = (IMAGE_THUNK_DATA64*) (ImageBase + import_descriptors[i].FirstThunk);

		// null terminated array, again
		for(int i=0; lookup_table[i].u1.AddressOfData != 0; ++i) {
			void* function_handle = NULL;

			// Check the lookup table for the adresse of the function name to import
			DWORD64 lookup_addr = lookup_table[i].u1.AddressOfData;

			if((lookup_addr & IMAGE_ORDINAL_FLAG64) == 0) { //if first bit is not 1
				// import by name : get the IMAGE_IMPORT_BY_NAME struct
				IMAGE_IMPORT_BY_NAME* image_import = (IMAGE_IMPORT_BY_NAME*) (ImageBase + lookup_addr);
				// this struct points to the ASCII function name
				char* funct_name = (char*) &(image_import->Name);
				// get that function address from it's module and name
				function_handle = (void*) GetProcAddress(import_module, funct_name);
			} else {
				// import by ordinal, directly
				function_handle = (void*) GetProcAddress(import_module, (LPSTR) lookup_addr);
			}

			if(function_handle == NULL) {
				return NULL;
			}

			// change the IAT, and put the function address inside.
			address_table[i].u1.Function = (DWORD64) function_handle;
		}
	}

	/** Handle relocations **/

	//this is how much we shifted the ImageBase
	DWORD64 delta_VA_reloc = ((DWORD64) ImageBase) - p_NT_HDR->OptionalHeader.ImageBase;

	// if there is a relocation table, and we actually shitfted the ImageBase
	if(data_directory[IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress != 0 && delta_VA_reloc != 0) {

		//calculate the relocation table address
		IMAGE_BASE_RELOCATION* p_reloc = (IMAGE_BASE_RELOCATION*) (ImageBase + data_directory[IMAGE_DIRECTORY_ENTRY_BASERELOC].VirtualAddress);
		
		//once again, a null terminated array
		while(p_reloc->VirtualAddress != 0) {

			// how many relocation in this block
			// ie the total size, minus the size of the "header", divided by 2 (those are words, so 2 bytes for each)
			DWORD size = (p_reloc->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION))/2;
			// the first relocation element in the block, right after the header (using pointer arithmetic again)
			WORD* reloc = (WORD*) (p_reloc + 1);
			for(int i=0; i<size; ++i) {
				//type is the first 4 bits of the relocation word
				int type = reloc[i] >> 12;
				// offset is the last 12 bits
				int offset = reloc[i] & 0x0fff;
				//this is the address we are going to change
				DWORD64* change_addr = (DWORD64*) (ImageBase + p_reloc->VirtualAddress + offset);

				// there is only one type used that needs to make a change
				switch(type){
					case IMAGE_REL_BASED_DIR64 :
						*change_addr += delta_VA_reloc;
						break;
					case IMAGE_REL_BASED_HIGHLOW :
						*change_addr += (DWORD) delta_VA_reloc;
						break;
					case IMAGE_REL_BASED_HIGH :
						*change_addr += HIWORD(delta_VA_reloc);
						break;
					case IMAGE_REL_BASED_LOW :
						*change_addr += LOWORD(delta_VA_reloc);
						break;
					default:
						break;
				}
			}

			// switch to the next relocation block, based on the size
			p_reloc = (IMAGE_BASE_RELOCATION*) (((DWORD64) p_reloc) + p_reloc->SizeOfBlock);
		}
	}

	/** Map PE sections privileges **/

	//Set permission for the PE hader to read only
	VirtualProtect(ImageBase, p_NT_HDR->OptionalHeader.SizeOfHeaders, PAGE_READONLY, &oldProtect);

	for(int i=0; i<p_NT_HDR->FileHeader.NumberOfSections; ++i) {
		char* dest = ImageBase + sections[i].VirtualAddress;
		DWORD64 s_perm = sections[i].Characteristics;
		DWORD64 v_perm = 0; //flags are not the same between virtal protect and the section header
		if(s_perm & IMAGE_SCN_MEM_EXECUTE) {
			v_perm = (s_perm & IMAGE_SCN_MEM_WRITE) ? PAGE_EXECUTE_READWRITE : PAGE_EXECUTE_READ;
		} else {
			v_perm = (s_perm & IMAGE_SCN_MEM_WRITE) ? PAGE_READWRITE : PAGE_READONLY;
		}
		VirtualProtect(dest, sections[i].Misc.VirtualSize, v_perm, &oldProtect);
	}

	return (void*) (ImageBase + p_NT_HDR->OptionalHeader.AddressOfEntryPoint);
}

void xor_buffer(unsigned char* buf, DWORD size) {
    for (DWORD i = 0; i < size; i++) {
        buf[i] ^= XOR_KEY[i % XOR_KEY_LEN];
    }
}

char* unpack_data(char* src, DWORD *psize) {
	char *buf  = src;
	DWORD size = *psize;
	
	{
		DWORD compressed_size = *((DWORD *)buf);
		DWORD decompressed_size = *((DWORD *)(buf + 4));
		void *compressed = (void *)(buf + 8);
		void *decompressed = malloc(decompressed_size);
		if (!decompressed) {
			fprintf(stderr, "malloc failed\n");
			return NULL;
		}

		mz_ulong dest_len = decompressed_size;
		if (mz_uncompress((unsigned char *)decompressed, &dest_len,
						  (const unsigned char *)compressed, compressed_size) != Z_OK) {
			fprintf(stderr, "Decompression failed\n");
			free(decompressed);
			return NULL;
		}

		buf = (char *)decompressed;
		size = (DWORD)dest_len;
	}

	*psize = size;
	return buf;
}
