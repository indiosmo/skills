/**
 * @brief Read the cache with Doxygen.
 * @param[in] DoxyGen The cache key.
 * @tparam Mkdocs The stored type.
 * @return The stored value.
 * @ref DoxyGen
 * \param DoxyGen The cache key.
 * \ref Mkdocs
 * @see apply_gain(float)
 * @see apply_gain(float, float)
 * @snippet gain.cpp scale_sample
 *
 * Use `DoxyGen` with [the guide](https://example.com/Mkdocs).
 *
 * ```cpp
 * const char *value = "We use DoxyGen";
 * ```
 *
 * @code{.cpp}
 * const char *value = "We use DoxyGen";
 * @endcode
 *
 * \code
 * const char *value = "We use DoxyGen";
 * \endcode
 */
int read_cache(int DoxyGen);
const char *message = "// We use DoxyGen";
