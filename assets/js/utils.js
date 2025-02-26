export const updateURLParams = (url, params) => {
    const _url = new URL(url);
    for (const key in params) {
        _url.searchParams.set(key, params[key]);
    }
    return _url;
};

export const asPercent = (value, total) => {
    const percent = (value / total) * 100;
    return Math.round(percent);
};

export const meters2km = (value) => {
    return Math.round(value / 1000);
};
