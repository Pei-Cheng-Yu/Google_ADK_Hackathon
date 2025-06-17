export function stringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  const c = (hash & 0x00FFFFFF).toString(16).toUpperCase();
  return lightenColor("#" + "00000".substring(0, 6 - c.length) + c);
}
export function lightenColor(hex, percent = 30) {
  const num = parseInt(hex.slice(1), 16);
  let r = (num >> 16) + Math.round(255 * (percent / 100));
  let g = ((num >> 8) & 0x00FF) + Math.round(255 * (percent / 100));
  let b = (num & 0x0000FF) + Math.round(255 * (percent / 100));

  r = Math.min(255, r);
  g = Math.min(255, g);
  b = Math.min(255, b);

  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}
// List of Tailwind background color classes to rotate through
const colorClasses = [
    'bg-violet-300',
    'bg-indigo-300',
    'bg-teal-300',
    'bg-green-300',
    'bg-lime-300',
    'bg-amber-300',
    'bg-orange-300',
    'bg-red-300',
];

/**
 * Convert a string (like goal_id) to a consistent index and return a Tailwind class
 */
export function goalIdToColorClass(goalId) {
  let hash = 0;
  for (let i = 0; i < goalId.length; i++) {
    hash = goalId.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % colorClasses.length;
  return colorClasses[index];
}
const colorLighterClasses = [
    'bg-violet-200',
    'bg-indigo-200',
    'bg-teal-200',
    'bg-green-200',
    'bg-lime-200',
    'bg-amber-200',
    'bg-orange-200',
    'bg-red-200',
];
const colorLighterClassesHash = [
    '#ddd6ff',
    '#c6d2ff',
    '#96f7e4',
    '#b9f8cf',
    '#d8f999',
    '#fee685',
    '#ffd6a8',
    '#ffa2a2',
];

/**
 * Convert a string (like goal_id) to a consistent index and return a Tailwind class
 */
export function goalIdToColorLighterClass(goalId) {
  let hash = 0;
  for (let i = 0; i < goalId.length; i++) {
    hash = goalId.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % colorClasses.length;
  return colorLighterClasses[index];
}
export function goalIdToColorLighterClassHash(goalId) {
  let hash = 0;
  for (let i = 0; i < goalId.length; i++) {
    hash = goalId.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % colorClasses.length;
  return colorLighterClassesHash[index];
}