import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';

export const myCustomTheme: CustomThemeConfig = {
    name: 'dimprotheme',
    properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `system-ui`,
		"--theme-font-family-heading": `system-ui`,
		"--theme-font-color-base": "0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "24px",
		"--theme-rounded-container": "24px",
		"--theme-border-base": "1px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "255 255 255",
		"--on-secondary": "255 255 255",
		"--on-tertiary": "0 0 0",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "255 255 255",
		"--on-surface": "255 255 255",
		// =~= Theme Colors  =~=
		// primary | #0E4889 
		"--color-primary-50": "219 228 237", // #dbe4ed
		"--color-primary-100": "207 218 231", // #cfdae7
		"--color-primary-200": "195 209 226", // #c3d1e2
		"--color-primary-300": "159 182 208", // #9fb6d0
		"--color-primary-400": "86 127 172", // #567fac
		"--color-primary-500": "14 72 137", // #0E4889
		"--color-primary-600": "13 65 123", // #0d417b
		"--color-primary-700": "11 54 103", // #0b3667
		"--color-primary-800": "8 43 82", // #082b52
		"--color-primary-900": "7 35 67", // #072343
		// secondary | #326094 
		"--color-secondary-50": "224 231 239", // #e0e7ef
		"--color-secondary-100": "214 223 234", // #d6dfea
		"--color-secondary-200": "204 215 228", // #ccd7e4
		"--color-secondary-300": "173 191 212", // #adbfd4
		"--color-secondary-400": "112 144 180", // #7090b4
		"--color-secondary-500": "50 96 148", // #326094
		"--color-secondary-600": "45 86 133", // #2d5685
		"--color-secondary-700": "38 72 111", // #26486f
		"--color-secondary-800": "30 58 89", // #1e3a59
		"--color-secondary-900": "25 47 73", // #192f49
		// tertiary | #8ea0b4 
		"--color-tertiary-50": "238 241 244", // #eef1f4
		"--color-tertiary-100": "232 236 240", // #e8ecf0
		"--color-tertiary-200": "227 231 236", // #e3e7ec
		"--color-tertiary-300": "210 217 225", // #d2d9e1
		"--color-tertiary-400": "176 189 203", // #b0bdcb
		"--color-tertiary-500": "142 160 180", // #8ea0b4
		"--color-tertiary-600": "128 144 162", // #8090a2
		"--color-tertiary-700": "107 120 135", // #6b7887
		"--color-tertiary-800": "85 96 108", // #55606c
		"--color-tertiary-900": "70 78 88", // #464e58
		// success | #84cc16 
		"--color-success-50": "237 247 220", // #edf7dc
		"--color-success-100": "230 245 208", // #e6f5d0
		"--color-success-200": "224 242 197", // #e0f2c5
		"--color-success-300": "206 235 162", // #ceeba2
		"--color-success-400": "169 219 92", // #a9db5c
		"--color-success-500": "132 204 22", // #84cc16
		"--color-success-600": "119 184 20", // #77b814
		"--color-success-700": "99 153 17", // #639911
		"--color-success-800": "79 122 13", // #4f7a0d
		"--color-success-900": "65 100 11", // #41640b
		// warning | #EAB308 
		"--color-warning-50": "252 244 218", // #fcf4da
		"--color-warning-100": "251 240 206", // #fbf0ce
		"--color-warning-200": "250 236 193", // #faecc1
		"--color-warning-300": "247 225 156", // #f7e19c
		"--color-warning-400": "240 202 82", // #f0ca52
		"--color-warning-500": "234 179 8", // #EAB308
		"--color-warning-600": "211 161 7", // #d3a107
		"--color-warning-700": "176 134 6", // #b08606
		"--color-warning-800": "140 107 5", // #8c6b05
		"--color-warning-900": "115 88 4", // #735804
		// error | #D41976 
		"--color-error-50": "249 221 234", // #f9ddea
		"--color-error-100": "246 209 228", // #f6d1e4
		"--color-error-200": "244 198 221", // #f4c6dd
		"--color-error-300": "238 163 200", // #eea3c8
		"--color-error-400": "225 94 159", // #e15e9f
		"--color-error-500": "212 25 118", // #D41976
		"--color-error-600": "191 23 106", // #bf176a
		"--color-error-700": "159 19 89", // #9f1359
		"--color-error-800": "127 15 71", // #7f0f47
		"--color-error-900": "104 12 58", // #680c3a
		// surface | #24384e 
		"--color-surface-50": "222 225 228", // #dee1e4
		"--color-surface-100": "211 215 220", // #d3d7dc
		"--color-surface-200": "200 205 211", // #c8cdd3
		"--color-surface-300": "167 175 184", // #a7afb8
		"--color-surface-400": "102 116 131", // #667483
		"--color-surface-500": "36 56 78", // #24384e
		"--color-surface-600": "32 50 70", // #203246
		"--color-surface-700": "27 42 59", // #1b2a3b
		"--color-surface-800": "22 34 47", // #16222f
		"--color-surface-900": "18 27 38", // #121b26
		
	}
}