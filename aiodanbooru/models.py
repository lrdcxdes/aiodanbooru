from typing import Optional, List

import aiohttp
from pydantic import BaseModel, Field, validator
from pydantic.networks import HttpUrl


class DanbooruPost(BaseModel):
    id: int
    uploader_id: int
    approver_id: Optional[int]
    tag_string: str
    tag_string_general: str
    tag_string_artist: str
    tag_string_copyright: str
    tag_string_character: str
    tag_string_meta: str
    rating: Optional[str]
    parent_id: Optional[int]
    source: Optional[str]
    md5: Optional[str] = Field(None, description="MD5 hash of the media file")
    file_url: Optional[HttpUrl] = Field(None, description="URL of the media file")
    large_file_url: Optional[HttpUrl] = Field(
        None, description="URL of the large version of the media file"
    )
    preview_file_url: Optional[HttpUrl] = Field(
        None, description="URL of the preview version of the media file"
    )
    file_ext: Optional[str]
    file_size: Optional[int]
    image_width: Optional[int]
    score: int
    fav_count: int
    tag_count_general: int
    tag_count_artist: int
    tag_count_copyright: int
    tag_count_character: int
    tag_count_meta: int
    last_comment_bumped_at: Optional[str]
    last_noted_at: Optional[str]
    has_children: bool
    image_height: Optional[int]
    created_at: str
    updated_at: str

    @validator("source")
    def validate_source(cls, source):
        if (
            source is not None
            and len(source) < 1
            and not cls.file_url
            and not cls.large_file_url
        ):
            raise ValueError("Source must have at least 1 character")
        return source

    class Config:
        extra = "allow"

    @property
    def extension(self) -> Optional[str]:
        if self.large_file_url:
            return self.large_file_url.split("/")[-1].split(".")[-1]
        elif self.file_url:
            return self.file_url.split("/")[-1].split(".")[-1]
        # elif self.source:
        #     return (
        #         self.source.split("/")[-1].split(".")[-1]
        #         if "." in self.source
        #         else self.file_ext
        #     )
        else:
            return self.file_ext

    async def get_media(self, use_large: bool = True) -> bytes:
        if not self.file_url and not self.large_file_url and self.source:
            return await self._get_media_from_source()
        url = (
            self.large_file_url if use_large and self.large_file_url else self.file_url
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()

    @property
    def tags(self) -> List[str]:
        return self.tag_string.split()

    @property
    def link(self):
        return f"https://danbooru.donmai.us/posts/{self.id}"

    @property
    def media_url(self):
        return (
            self.large_file_url if self.large_file_url else self.file_url or self.source
        )

    def is_video(self) -> bool:
        return self.extension in ["webm", "mp4"]

    def is_image(self) -> bool:
        return self.extension in ["jpg", "jpeg", "png", "webp"]

    def is_animation(self) -> bool:
        return self.extension in ["gif", "gifv"]

    def is_zip(self) -> bool:
        return self.extension in ["zip"]

    @property
    def filename(self):
        return f"{self.md5}.{self.extension}"

    async def _get_media_from_source(self):
        async with aiohttp.ClientSession() as session:
            if self.source.startswith("https://i.pximg.net"):
                url = self.source.replace("i.pximg.net", "i.pixiv.cat")
            elif self.source.startswith("file://"):
                return b""
            else:
                url = self.source
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
