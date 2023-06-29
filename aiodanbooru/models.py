from typing import Optional

import aiohttp
from pydantic import BaseModel, Field


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
    md5: str
    file_url: str
    large_file_url: str
    preview_file_url: str
    file_ext: str
    file_size: int
    image_width: int
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
    image_height: int
    created_at: str
    updated_at: str

    class Config:
        extra = "allow"

    extension: Optional[str] = Field(None, alias="file_ext")

    async def get_media(self, use_large: bool = True) -> bytes:
        url = (
            self.large_file_url if use_large and self.large_file_url else self.file_url
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()

    @property
    def link(self):
        return f"https://danbooru.donmai.us/posts/{self.id}"

    @property
    def media_url(self):
        return self.large_file_url if self.large_file_url else self.file_url

    def is_video(self) -> bool:
        return self.extension in ["webm", "mp4"]

    def is_image(self) -> bool:
        return self.extension in ["jpg", "jpeg", "png", "gif"]

    @property
    def filename(self):
        return f"{self.md5}.{self.extension}"
