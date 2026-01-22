tailwind.config = {
    darkMode: 'class',
    theme: {
        fontFamily: {
            sans: ['Roboto', 'sans-serif'],
        },
        extend: {
            colors: {
                violet: {
                    600: '#7C3AED',
                    700: '#6D28D9',
                    800: '#5B21B6',
                    900: '#4C1D95',
                }
            },
            animation: {
                'bounce-slow': 'bounce 2s infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' },
                }
            }
        }
    }
}
