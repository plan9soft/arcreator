#ifndef ZER0_CODE_SNIPPETS_H
#define ZER0_CODE_SNIPPETS_H

// iterator macro
#define for_iter(name, min, max) for (int name = min; name < max; name++)

#define RB_VAR2CPP(type, name) type* name; Data_Get_Struct(self, type, name);

#endif