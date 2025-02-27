export const updateURLParams = (url, params) => {
    const _url = new URL(url);
    for (const key in params) {
        _url.searchParams.set(key, params[key]);
    }
    return _url;
};

export const round = (value, precision) => {
    const multiplier = Math.pow(10, precision || 0);
    return Math.round(value * multiplier) / multiplier;
};

export const asPercent = (value, total, precision = 0) => {
    const percent = (value / total) * 100;
    return round(percent, precision);
};

export const meters2km = (value, precision = 1) => {
    return round(value / 1000, precision);
};
