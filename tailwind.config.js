//add custom classes here

module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
    // defaultLineHeights: true,
    // standardFontWeights: true
  },
  purge: [],
  theme: {
    extend: {
      keyframes: {
        'wiggle': {
        '0%, 100%': { transform: 'rotate(-3deg)' },
        '50%': { transform: 'rotate(3deg)' },
        }
      },
       animation: {
        'wiggle': 'wiggle 1s ease-in-out infinite',
      }
    }
  },
  variants: {},
  plugins: []
}
