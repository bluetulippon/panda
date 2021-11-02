// **** libc ****

void delay(uint32_t a) {
  volatile uint32_t i;
  for (i = 0; i < a; i++);
}

void *memset(void *str, int c, unsigned int n) {
  uint8_t *s = str;
  for (unsigned int i = 0; i < n; i++) {
    *s = c;
    s++;
  }
  return str;
}

void *memcpy(void *pDest, const void *pSrc, unsigned int len) {
  uint32_t numLongs = len / 4U;
  uint32_t trailBytes = len & 0x03U;

  const uint32_t *pLongSrc = (const uint32_t*) pSrc;
  uint32_t *pLongDest = (uint32_t*) pDest;

  // let processor handle any 32-bit alignment issues
  while (numLongs-- > 0) {
    *pLongDest = *pLongSrc;
     pLongDest++;
     pLongSrc++;
  }

  const uint8_t *pCharSrc = (const uint8_t*) pLongSrc;
  uint8_t *pCharDest = (uint8_t*) pLongDest;

  while (trailBytes-- > 0) {
    *pCharDest = *pCharSrc;
    pCharDest++;
    pCharSrc++;
  }
  return pDest;
}

int memcmp(const void * ptr1, const void * ptr2, unsigned int num) {
  int ret = 0;
  const uint8_t *p1 = ptr1;
  const uint8_t *p2 = ptr2;
  for (unsigned int i = 0; i < num; i++) {
    if (*p1 != *p2) {
      ret = -1;
      break;
    }
    p1++;
    p2++;
  }
  return ret;
}
