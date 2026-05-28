/** @type {import(''prettier'').Config} */

const config = {
  plugins: [require.resolve("@prettier/plugin-xml")],
  bracketSpacing: false,
  printWidth: 120,
  proseWrap: "always",
  semi: true,
  trailingComma: "es5",
  xmlWhitespaceSensitivity: "preserve",
};

module.exports = config;
