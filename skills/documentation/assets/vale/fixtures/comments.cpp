const char *message = "// Simply utilize DoxyGen";

/**
 * @brief We read the cache.
 * @param DoxyGen Use the cache key.
 * @return The stored value.
 *
 * Use `DoxyGen` with [the guide](https://example.com/Mkdocs).
 *
 * @code
 * const char *value = "Simply utilize DoxyGen";
 * @endcode
 */
int read_cache(int DoxyGen);

/// We use DoxyGen.
int read_documented_cache();

//! We use Mkdocs.
int read_alternative_cache();

int cached_value; ///< We use DoxyGen.

/* Ordinary comments also describe behavior. We use the cache. */
